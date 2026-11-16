import csv
import json
from collections import Counter
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CURRENT_DATA = ROOT / "datos_viirs_san_martin_2024_2026.json"
OUTPUT_DATA = ROOT / "datos_viirs_san_martin_2021_2026.json"
MAP_FILE = ROOT / "incendios.html"
SOURCES = {
    "2021": [
        Path(r"DL_FIRE_SV-C2_851156\fire_archive_SV-C2_851156.csv"),
    ],
    "2022": [
        Path(r"DL_FIRE_SV-C2_851154\fire_archive_SV-C2_A.csv"),
        Path(r"DL_FIRE_SV-C2_851154\fire_archive_SV-C2_B.csv"),
    ],
    "2023": [
        Path(r"DL_FIRE_SV-C2_851152\fire_archive_SV-C2_851152.csv"),
        Path(r"DL_FIRE_J2V-C2_851151\fire_archive_J2V-C2_851151.csv"),
    ],
}


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


def date_periods(dates):
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


def read_source(path, ring, records, source_dates, satellite_counts):
    full_path = ROOT / path
    if not full_path.is_file():
        raise FileNotFoundError(f"No se encontró el archivo fuente: {full_path}")

    min_lon = min(point[0] for point in ring)
    max_lon = max(point[0] for point in ring)
    min_lat = min(point[1] for point in ring)
    max_lat = max(point[1] for point in ring)
    retained = 0
    print(f"Procesando {path}...", flush=True)
    with full_path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        required = {"latitude", "longitude", "acq_date", "acq_time", "satellite", "confidence", "frp"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f"El CSV {path} no contiene las columnas FIRMS esperadas.")
        for row in reader:
            acquisition_date = row["acq_date"]
            if not acquisition_date:
                continue
            source_dates.add(acquisition_date)
            latitude = float(row["latitude"])
            longitude = float(row["longitude"])
            if not (min_lat <= latitude <= max_lat and min_lon <= longitude <= max_lon):
                continue
            if not point_in_ring(latitude, longitude, ring):
                continue

            confidence = row["confidence"].strip().lower()
            satellite = row["satellite"].strip().upper()
            if confidence not in {"l", "n", "h"}:
                raise ValueError(f"Confianza VIIRS no reconocida en {path}: {confidence!r}")
            if satellite not in {"N20", "N21", "SNPP"}:
                raise ValueError(f"Satélite VIIRS no reconocido en {path}: {satellite!r}")
            acquisition_time = row["acq_time"].strip().zfill(4)
            frp = float(row["frp"]) if row["frp"] else None
            records.append([
                latitude,
                longitude,
                acquisition_date,
                acquisition_time,
                frp,
                confidence,
                satellite,
                None,
                None,
                None,
            ])
            satellite_counts[satellite] += 1
            retained += 1
    print(f"  {retained:,} detecciones dentro de San Martín.", flush=True)


def main():
    existing = json.loads(CURRENT_DATA.read_text(encoding="utf-8"))
    ring = load_boundary_ring()
    records_by_year = {year: [] for year in SOURCES}
    coverage = {}

    for year, paths in SOURCES.items():
        source_dates = set()
        satellite_counts = Counter()
        for path in paths:
            read_source(path, ring, records_by_year[year], source_dates, satellite_counts)
        records = records_by_year[year]
        records.sort(key=lambda row: (row[2], row[3], row[6], row[0], row[1]))
        coverage[year] = {
            "count": len(records),
            "from": min((record[2] for record in records), default=None),
            "to": max((record[2] for record in records), default=None),
            "satellites": dict(sorted(satellite_counts.items())),
            "files": [path.as_posix() for path in paths],
            "data_through": max(source_dates, default=None),
            "coverage_periods": date_periods(source_dates),
        }
        print(
            f"{year}: {len(records):,} detecciones; "
            f"{len(coverage[year]['coverage_periods'])} periodos de cobertura.",
            flush=True,
        )

    for year, records in existing["records"].items():
        records_by_year[year] = records
    merged_coverage = {**coverage, **existing["coverage"]}
    output = {
        "boundary": existing["boundary"],
        "records": records_by_year,
        "coverage": merged_coverage,
    }
    OUTPUT_DATA.write_text(
        json.dumps(output, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    print(f"Dataset consolidado guardado en {OUTPUT_DATA.name}.", flush=True)


if __name__ == "__main__":
    main()
