"""Consolidate VIIRS detections with locally available MODIS active-fire files.

The output uses a common 12-field record while retaining sensor provenance.
It is a harmonized schema, not a cross-sensor radiometric calibration.
"""

import csv
import io
import json
from collections import Counter
from datetime import date, timedelta
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parent
VIIRS_FILE = ROOT / "datos_viirs_san_martin_2021_2026.json"
OUTPUT_FILE = ROOT / "datos_focos_harmonizados_2021_2026.json"
MAP_FILE = ROOT / "incendios.html"

def discover_modis_files():
    files = set()
    patterns = [
        "fire_archive_M-C61_*.csv", "fire_nrt_M-C61_*.csv",
        "DL_FIRE_M-C61_*/fire_archive_M-C61_*.csv", "DL_FIRE_M-C61_*/fire_nrt_M-C61_*.csv",
        "MODIS/**/fire_archive_M-C61_*.csv", "MODIS/**/fire_nrt_M-C61_*.csv",
    ]
    for pattern in patterns:
        files.update(ROOT.glob(pattern))
    sources = [(path, None) for path in sorted(files)]
    archives = set(ROOT.glob("MODIS/DL_FIRE_M-C61_*.zip")) | set(ROOT.glob("DL_FIRE_M-C61_*.zip"))
    for archive in sorted(archives):
        with ZipFile(archive) as zipped:
            for member in zipped.namelist():
                name = Path(member).name
                if name.startswith(("fire_archive_M-C61_", "fire_nrt_M-C61_")) and name.endswith(".csv"):
                    sources.append((archive, member))
    return sources


MODIS_FILES = discover_modis_files()


def source_label(path, member=None):
    relative = path.relative_to(ROOT).as_posix()
    return f"{relative}!{member}" if member else relative


def open_source(path, member=None):
    if member:
        archive = ZipFile(path)
        binary = archive.open(member)
        return archive, io.TextIOWrapper(binary, encoding="utf-8-sig", newline="")
    return None, path.open("r", encoding="utf-8-sig", newline="")


def load_boundary_ring():
    source = MAP_FILE.read_text(encoding="utf-8")
    marker = "san_martin_boundary_layer = L.geoJSON("
    start = source.index(marker) + len(marker)
    feature, _ = json.JSONDecoder().raw_decode(source[start:].lstrip())
    return feature["geometry"]["coordinates"][0]


def point_in_ring(latitude, longitude, ring):
    inside = False
    previous_lon, previous_lat = ring[-1]
    for current_lon, current_lat in ring:
        crosses = (current_lat > latitude) != (previous_lat > latitude) and longitude < (
            (previous_lon - current_lon) * (latitude - current_lat)
            / (previous_lat - current_lat) + current_lon
        )
        if crosses:
            inside = not inside
        previous_lon, previous_lat = current_lon, current_lat
    return inside


def compress_dates(dates):
    ordered = sorted(date.fromisoformat(value) for value in dates)
    if not ordered:
        return []
    periods = []
    start = previous = ordered[0]
    for current in ordered[1:]:
        if current != previous + timedelta(days=1):
            periods.append([start.isoformat(), previous.isoformat()])
            start = current
        previous = current
    periods.append([start.isoformat(), previous.isoformat()])
    return periods


def expand_periods(periods):
    dates = set()
    for first, last in periods:
        day = date.fromisoformat(first)
        end = date.fromisoformat(last)
        while day <= end:
            dates.add(day.isoformat())
            day += timedelta(days=1)
    return dates


def modis_confidence(value):
    score = int(float(value)) if value not in (None, "") else 0
    # FIRMS MODIS confidence classes: low <30, nominal 30–79, high >=80.
    label = "l" if score < 30 else "n" if score < 80 else "h"
    return label, score


def read_modis(ring):
    if not MODIS_FILES:
        raise FileNotFoundError("No se encontraron archivos FIRMS MODIS C6.1 en DL_FIRE_M-C61_*/.")
    records = []
    regional_dates = set()
    input_dates = set()
    source_counts = Counter()
    min_lon = min(point[0] for point in ring)
    max_lon = max(point[0] for point in ring)
    min_lat = min(point[1] for point in ring)
    max_lat = max(point[1] for point in ring)
    seen = set()

    for path, member in MODIS_FILES:
        if not path.is_file():
            raise FileNotFoundError(f"Falta el archivo MODIS: {source_label(path, member)}")
        label = source_label(path, member)
        print(f"Procesando {label}...", flush=True)
        archive, handle = open_source(path, member)
        try:
            reader = csv.DictReader(handle)
            required = {"latitude", "longitude", "acq_date", "acq_time", "satellite", "confidence", "frp"}
            if not required.issubset(reader.fieldnames or []):
                raise ValueError(f"El archivo {path.name} no tiene las columnas FIRMS esperadas.")
            for row in reader:
                acquired = row.get("acq_date", "")
                if not acquired:
                    continue
                input_dates.add(acquired)
                # Exclude non-vegetation thermal anomalies when FIRMS supplies a type.
                if row.get("type") not in (None, "", "0"):
                    continue
                latitude = float(row["latitude"])
                longitude = float(row["longitude"])
                if not (min_lat <= latitude <= max_lat and min_lon <= longitude <= max_lon):
                    continue
                if not point_in_ring(latitude, longitude, ring):
                    continue
                satellite = row.get("satellite", "MODIS").strip().title()
                time = row.get("acq_time", "").strip().zfill(4)
                # FIRMS archive and NRT may overlap; drop exact repeated observations.
                key = (round(latitude, 5), round(longitude, 5), acquired, time, satellite)
                if key in seen:
                    continue
                seen.add(key)
                confidence, score = modis_confidence(row.get("confidence"))
                frp = float(row["frp"]) if row.get("frp") else None
                records.append([
                    latitude, longitude, acquired, time, frp, confidence, satellite,
                    None, None, None, "MODIS", score,
                ])
                regional_dates.add(acquired)
                source_counts[satellite] += 1
        finally:
            handle.close()
            if archive:
                archive.close()

    records.sort(key=lambda row: (row[2], row[3], row[6], row[0], row[1]))
    print(f"MODIS: {len(records):,} focos regionales; {len(regional_dates):,} fechas con detecciones.", flush=True)
    if not input_dates:
        raise ValueError("Los CSV MODIS no contienen fechas de adquisición.")
    return records, regional_dates, input_dates, source_counts


def main():
    viirs = json.loads(VIIRS_FILE.read_text(encoding="utf-8"))
    ring = load_boundary_ring()
    records = {}
    coverage = {}

    for year, year_records in viirs["records"].items():
        records[year] = [list(record) + ["VIIRS", None] for record in year_records]
        source_coverage = viirs["coverage"][year]
        viirs_count = len(year_records)
        viirs_periods = source_coverage.get("coverage_periods") or []
        if not viirs_periods and viirs_count:
            source_start = source_coverage.get("source_from") or f"{year}-01-01"
            source_end = source_coverage.get("data_through") or source_coverage.get("to")
            if source_end:
                viirs_periods = [[source_start, source_end]]
        coverage[year] = {
            **source_coverage,
            "viirs_coverage_periods": viirs_periods,
            "modis_coverage_periods": [],
            "viirs_count": viirs_count,
            "modis_count": 0,
            "source_counts": {"VIIRS": viirs_count},
            "sensors": ["VIIRS"],
        }

    modis_records, modis_dates, all_modis_dates, satellite_counts = read_modis(ring)
    modis_by_year = Counter(record[2][:4] for record in modis_records)
    for record in modis_records:
        year = record[2][:4]
        records.setdefault(year, []).append(record)
    for year in sorted(records):
        records[year].sort(key=lambda row: (
            row[2], row[3] or "", row[10] or "", row[6] or "", row[0], row[1],
        ))
        coverage.setdefault(year, {
            "count": 0, "from": None, "to": None, "satellites": {},
            "files": [], "data_through": None, "coverage_periods": [],
            "viirs_count": 0, "modis_count": 0, "source_counts": {"VIIRS": 0}, "sensors": [],
        })
        meta = coverage[year]
        modis_count = modis_by_year[year]
        meta["viirs_count"] = meta.get("viirs_count", 0)
        meta["modis_count"] = modis_count
        meta["count"] = meta["viirs_count"] + modis_count
        meta["source_counts"] = {"VIIRS": meta["viirs_count"], "MODIS": modis_count}
        meta["sensors"] = [sensor for sensor in ("MODIS", "VIIRS") if meta["source_counts"][sensor]]
        year_source_dates = sorted(d for d in all_modis_dates if d.startswith(year))
        if year_source_dates:
            meta["modis_coverage_periods"] = compress_dates(year_source_dates)
        if modis_count:
            year_modis_dates = sorted(d for d in modis_dates if d.startswith(year))
            first_modis, last_modis = year_modis_dates[0], year_modis_dates[-1]
            meta["from"] = min(filter(None, [meta.get("from"), first_modis]), default=first_modis)
            meta["to"] = max(filter(None, [meta.get("to"), last_modis]), default=last_modis)
            meta["data_through"] = max(filter(None, [meta.get("data_through"), year_source_dates[-1]]), default=last_modis)
            meta["modis_files"] = [source_label(path, member) for path, member in MODIS_FILES]
            meta["modis_satellites"] = dict(sorted(Counter(
                record[6] for record in records[year] if record[10] == "MODIS"
            ).items()))
        all_dates = expand_periods(meta.get("viirs_coverage_periods", [])).union(
            expand_periods(meta.get("modis_coverage_periods", []))
        )
        meta["coverage_periods"] = compress_dates(all_dates)

    output = {
        "boundary": viirs["boundary"],
        "records": records,
        "coverage": coverage,
        "record_fields": [
            "latitude", "longitude", "date", "time_utc", "frp_mw", "confidence_class",
            "satellite", "locality", "distance_km", "province", "sensor", "confidence_score",
        ],
        "harmonization": {
            "schema": "common hotspot observation record; raw source retained in sensor field",
            "modis_confidence": "FIRMS numeric confidence mapped to l (<30), n (30–79), h (>=80)",
            "modis_detection_type": "Only FIRMS type 0 presumed vegetation fires retained",
            "duplicate_policy": "Exact MODIS archive/NRT duplicates removed; cross-sensor detections retained",
            "limitation": "This standardizes fields; it does not calibrate sensor sensitivity or equate detection counts across MODIS and VIIRS.",
            "modis_files": [source_label(path, member) for path, member in MODIS_FILES],
            "modis_source_dates": [min(all_modis_dates), max(all_modis_dates)],
        },
    }
    OUTPUT_FILE.write_text(json.dumps(output, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"Dataset armonizado guardado en {OUTPUT_FILE.name}.", flush=True)


if __name__ == "__main__":
    main()
