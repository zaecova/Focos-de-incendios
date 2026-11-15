# Documentación del mapa de incendios forestales

## Propósito

Este proyecto presenta detecciones satelitales VIIRS para la región San Martín. Es una herramienta de consulta histórica; no representa la situación actual ni confirma por sí sola incendios.

## Uso del mapa

1. Arrastra el mapa para desplazarte y usa los controles **+** y **−** para acercar o alejar.
2. Abre **Capas** para activar o desactivar las detecciones, las capas de densidad y el límite departamental de San Martín.
3. Usa los filtros de año, mes y confianza de la página para acotar los puntos y el calendario; los cambios actualizan el mapa OpenStreetMap.
4. Pulsa **Dibujar área en el mapa**, traza un polígono y cierra su contorno para limitar los resultados a esa zona. **Quitar área** restaura toda la región.
5. El calendario muestra la intensidad diaria; pulsa una fecha para filtrar el mapa por ese día y **Quitar día** para volver al intervalo elegido.
6. Pasa el cursor sobre un marcador con nombre para ver la localidad cercana; selecciónalo para consultar todos sus detalles.

## Capas y leyenda

- **Puntos VIIRS · FRP (MW):** el color indica la potencia radiativa del fuego (FRP) registrada por VIIRS:
  - Verde: hasta 20 MW.
  - Naranja: más de 20 y hasta 50 MW.
  - Rojo: más de 50 MW.
- **Detecciones 2024:** cobertura anual de San Martín combinando NOAA-20, NOAA-21 y Suomi-NPP.
- **Detecciones 2025:** 23.273 registros combinados de NOAA-20, NOAA-21 y Suomi-NPP.
- **Detecciones 2026:** NOAA-21 y Suomi-NPP; la parte más reciente procede de datos near-real-time.
- **Mancha de calor:** muestra la concentración de detecciones de la capa correspondiente; no representa una probabilidad de incendio.
- **Límite departamental:** al seleccionar el contorno se muestra el nombre del lugar (San Martín), su nivel administrativo y la atribución de la fuente geoBoundaries.

## Calendario y patrones históricos

- El calendario interactivo resume detecciones por día para el año seleccionado y admite selección directa de una fecha. Los días posteriores al 7 de noviembre de 2026 se muestran como **sin cobertura**, no como días sin detecciones.
- El gráfico compara el promedio diario de detecciones de cada mes entre 2024, 2025 y 2026. Se actualiza al cambiar el polígono o el nivel de confianza; el calendario y el mapa responden además a los filtros de año, mes y día.
- Se marca como **actividad elevada** el mes completo de 2026 cuyo promedio diario sea al menos 50 % mayor que el promedio del mismo mes en 2024 y 2025. Es un criterio descriptivo de comparación, no una alerta oficial ni una explicación meteorológica.
- Noviembre de 2026 está incompleto: las detecciones regionales llegan al día 5 y los archivos fuente al día 7. No se incluye en el cálculo de meses destacados.

## Cobertura de los datos

- **2024:** 40.482 detecciones dentro de San Martín, del 2 de enero al 30 de diciembre; NOAA-20: 13.815, NOAA-21: 13.822 y Suomi-NPP: 12.845.
- **2025:** 23.273 detecciones dentro de San Martín, del 1 de enero al 31 de diciembre; NOAA-20: 7.650, NOAA-21: 7.814 y Suomi-NPP: 7.809.
- **2026:** 13.611 detecciones dentro de San Martín, del 1 de enero al 5 de noviembre; NOAA-21: 6.802 y Suomi-NPP: 6.809. Los archivos fuente llegan hasta el 7 de noviembre; no hubo detecciones regionales el 6 y 7 de noviembre. Incluye datos de archivo hasta julio y datos near-real-time después de ese periodo, que pueden ser revisados por NASA FIRMS.

Los conteos son detecciones satelitales, no incendios únicos confirmados. Un mismo foco puede ser detectado más de una vez o por varios satélites; no se deduplicaron observaciones entre sensores.
La cobertura de 2026 es parcial, por lo que su total no es directamente comparable con los años completos.

## Detalles de los marcadores

Los registros muestran fecha, hora disponible, coordenadas, FRP, confianza VIIRS y satélite. Cuando la fuente contiene esa información, el punto muestra la provincia y la localidad poblada más cercana, junto con su distancia aproximada. La localidad es una referencia geográfica, no necesariamente el lugar exacto de la detección. Hay nombres para 1.331 registros de 2024, incorporados al coincidir exactamente fecha y coordenadas con puntos previamente identificados, y para 7.650 registros NOAA-20 de 2025. Los CSV de 2026 no incluyen localidades. En los demás casos, el popup indica que el nombre no está disponible en los datos.

## Fuentes

- [NASA FIRMS — datos VIIRS](https://firms.modaps.eosdis.nasa.gov/download/) (NOAA-20, NOAA-21 y Suomi-NPP).
- Archivos CSV FIRMS publicados en el repositorio y conjunto regional procesado en `datos_viirs_san_martin_2024_2026.json`.
- [geoBoundaries — límites provinciales del Perú](https://github.com/wmgeolab/geoBoundaries/tree/9469f09/releaseData/gbOpen/PER/ADM2).
- [GeoNames — referencia geográfica de localidades](https://www.geonames.org/).
