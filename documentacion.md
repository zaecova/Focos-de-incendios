# Documentación del mapa de incendios forestales

## Propósito

Este proyecto presenta detecciones satelitales VIIRS para Perú y la región San Martín. Es una herramienta de consulta histórica; no representa la situación actual ni confirma por sí sola incendios.

## Uso del mapa

1. Arrastra el mapa para desplazarte y usa los controles **+** y **−** para acercar o alejar.
2. Abre **Capas** para activar o desactivar las detecciones, las capas de densidad y el límite departamental de San Martín.
3. Selecciona un marcador para consultar sus detalles.

## Capas y leyenda

- **Puntos VIIRS · FRP (MW):** el color indica la potencia radiativa del fuego (FRP) registrada por VIIRS:
  - Verde: hasta 20 MW.
  - Naranja: más de 20 y hasta 50 MW.
  - Rojo: más de 50 MW.
- **Detecciones 2024:** cobertura anual de San Martín combinando NOAA-20, NOAA-21 y Suomi-NPP.
- **Detecciones 2025:** los 7.650 registros NOAA-20 existentes y una capa adicional con 15.623 registros NOAA-21/Suomi-NPP.
- **Detecciones 2026:** NOAA-21 y Suomi-NPP; la parte más reciente procede de datos near-real-time.
- **Mancha de calor:** muestra la concentración de detecciones de la capa correspondiente; no representa una probabilidad de incendio.
- **Densidad VIIRS · Perú · 6 fechas de 2024:** capa histórica nacional, distinta de la cobertura anual de San Martín.
- **Límite departamental:** contorno de referencia de la región San Martín.

## Cobertura de los datos

- **2024:** 40.482 detecciones dentro de San Martín, del 2 de enero al 30 de diciembre; NOAA-20: 13.815, NOAA-21: 13.822 y Suomi-NPP: 12.845.
- **2025:** 23.273 detecciones dentro de San Martín, del 1 de enero al 31 de diciembre; NOAA-20: 7.650, NOAA-21: 7.814 y Suomi-NPP: 7.809.
- **2026:** 13.611 detecciones dentro de San Martín, del 1 de enero al 5 de noviembre; NOAA-21: 6.802 y Suomi-NPP: 6.809. Incluye datos de archivo hasta julio y datos near-real-time después de ese periodo, que pueden ser revisados por NASA FIRMS.

Los conteos son detecciones satelitales, no incendios únicos confirmados. Un mismo foco puede ser detectado más de una vez o por varios satélites; no se deduplicaron observaciones entre sensores.
La cobertura de 2026 es parcial, por lo que su total no es directamente comparable con los años completos.

## Detalles de los marcadores

Los nuevos registros muestran fecha, hora, coordenadas, FRP, confianza VIIRS y satélite. Los registros NOAA-20 existentes de 2025 también incluyen provincia y la localidad poblada más cercana; la localidad es una referencia geográfica y no necesariamente el lugar exacto de la detección, y la distancia es aproximada.

## Fuentes

- [NASA FIRMS — datos VIIRS](https://firms.modaps.eosdis.nasa.gov/download/) (NOAA-20, NOAA-21 y Suomi-NPP).
- Archivos CSV FIRMS publicados en el repositorio y conjunto regional procesado en `datos_viirs_san_martin_2024_2026.json`.
- [geoBoundaries — límites provinciales del Perú](https://github.com/wmgeolab/geoBoundaries/tree/9469f09/releaseData/gbOpen/PER/ADM2).
- [GeoNames — referencia geográfica de localidades](https://www.geonames.org/).
