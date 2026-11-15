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
- **Mancha de calor:** muestra la concentración de detecciones de la capa activa; no representa una probabilidad de incendio.
- **Límite departamental:** contorno de referencia de la región San Martín.

## Cobertura de los datos

- **2024:** 10.584 detecciones de todo el Perú en seis fechas seleccionadas: 30 de agosto y 3, 8, 13, 14 y 18 de septiembre.
- **2025:** 7.650 detecciones del año completo dentro de la región San Martín.

Los años tienen periodos y coberturas diferentes, por lo que sus cantidades no se deben comparar directamente.

## Detalles de los marcadores

Según la detección, el popup puede mostrar fecha, coordenadas, FRP, confianza VIIRS, provincia y la localidad poblada más cercana. La localidad es una referencia geográfica y no necesariamente el lugar exacto de la detección; la distancia es aproximada.

## Fuentes

- [NASA FIRMS — datos VIIRS](https://firms.modaps.eosdis.nasa.gov/download/) (JPSS-1 / NOAA-20).
- [geoBoundaries — límites provinciales del Perú](https://github.com/wmgeolab/geoBoundaries/tree/9469f09/releaseData/gbOpen/PER/ADM2).
- [GeoNames — referencia geográfica de localidades](https://www.geonames.org/).
