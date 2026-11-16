# Documentación del mapa de incendios forestales

## Propósito

Este proyecto organiza detecciones satelitales VIIRS en un calendario de actividad de focos de calor para la región San Martín entre 2021 y 2026. También presenta un resumen meteorológico separado para 2021–2026; el clima aporta contexto, no detecciones de incendios. Permite explorar patrones históricos, condiciones inusuales y periodos críticos en un área seleccionada, mediante filtros de fecha, confianza y polígono dibujado. Está pensado como apoyo para la consulta y el análisis; no representa la situación actual ni confirma por sí sola incendios.

## Uso del mapa

1. Arrastra el mapa para desplazarte y usa los controles **+** y **−** para acercar o alejar.
2. Abre **Capas** para activar o desactivar las detecciones, las capas de densidad y el límite departamental de San Martín.
3. Usa los filtros de año, mes y confianza de la página para acotar los puntos y el calendario; los cambios actualizan el mapa OpenStreetMap. El selector dentro del calendario permite elegir directamente un año de 2021 a 2026. El calendario usa colores VIIRS en las fechas cubiertas y temperatura diaria cuando no hay cobertura de detecciones; 2022 tiene solo cobertura VIIRS parcial.
4. Pulsa **Dibujar área en el mapa**, traza un polígono y cierra su contorno para limitar los resultados a esa zona. **Quitar área** restaura toda la región.
5. El calendario muestra la intensidad diaria; pulsa una fecha para filtrar el mapa por ese día y consultar detecciones, temperatura, probabilidad histórica de precipitación y días secos. **Quitar día** vuelve al intervalo elegido.
6. Pasa el cursor sobre un marcador con nombre para ver la localidad cercana; selecciónalo para consultar todos sus detalles.

## Capas y leyenda

- **Puntos VIIRS · FRP (MW):** el color indica la potencia radiativa del fuego (FRP) registrada por VIIRS:
  - Verde: hasta 20 MW.
  - Naranja: más de 20 y hasta 50 MW.
  - Rojo: más de 50 MW.
- **Detecciones 2021:** archivo anual de Suomi-NPP.
- **Detecciones 2022:** 394 detecciones de Suomi-NPP en las fechas disponibles del archivo: 1–6 y 15–19 de enero. No se debe interpretar el resto del año como cobertura sin focos.
- **Detecciones 2023:** archivos anuales disponibles de Suomi-NPP y NOAA-21.
- **Detecciones 2024–2025:** NOAA-20, NOAA-21 y Suomi-NPP.
- **Detecciones 2026:** NOAA-21 y Suomi-NPP; datos regionales hasta el 5 de noviembre y fuentes hasta el 7 de noviembre.
- El mapa presenta el total de registros disponibles por año. Una detección no equivale a un incendio único y satélites distintos pueden observar el mismo foco.
- **Mancha de calor:** muestra la concentración de detecciones de la capa correspondiente; no representa una probabilidad de incendio.
- **Límite departamental:** al seleccionar una zona del mapa se consulta el nombre geográfico cercano mediante OpenStreetMap; el popup también muestra la provincia, departamento y coordenadas. El nombre es una referencia aproximada y requiere conexión a internet.

## Calendario y patrones históricos

- El panel **Resumen de actividad reciente** indica el intervalo de siete días más reciente incluido en 2026, el total y el promedio diario de detecciones en el área y nivel de confianza elegidos, y la referencia diaria para las mismas fechas de 2024 y 2025. Muestra por separado hasta qué fecha llegan las detecciones y hasta cuál llegan los archivos fuente.
- El panel muestra un aviso experimental cuando el intervalo tiene al menos cinco detecciones y su promedio diario es al menos 50 % mayor que la referencia de 2024–2025. El aviso es retrospectivo: no vigila datos en vivo, no predice incendios, no descarta peligro cuando no se activa y no es una alerta oficial. Los datos VIIRS son detecciones satelitales, no incendios confirmados.
- El calendario interactivo resume detecciones por día para el año seleccionado y admite selección directa de una fecha. En fechas cubiertas sin registros regionales, el calendario indica cero detecciones; en fechas sin cobertura muestra temperatura si hay datos meteorológicos. Los días posteriores al 7 de noviembre de 2026 se muestran como **sin cobertura**, no como días sin detecciones.
- Al seleccionar un día, el calendario muestra el total de detecciones VIIRS, la temperatura media/máxima/mínima, la precipitación diaria, la probabilidad histórica de precipitación cuando está disponible y la racha consecutiva de días secos. El conteo de detecciones respeta el área y la confianza seleccionadas; el clima siempre representa el promedio regional de San Martín.
- El promedio meteorológico simple usa cuatro localidades de referencia: Moyobamba, Tarapoto, Juanjuí y Tocache. Temperatura, humedad relativa, viento, precipitación diaria y humedad del suelo provienen del reanálisis ERA5-Land de Open-Meteo. La probabilidad es el promedio de `precipitation_probability_max` en el archivo de pronósticos históricos de Open-Meteo; no es una probabilidad actual ni se infiere de la lluvia observada. CAPE también procede del archivo de pronósticos históricos. Cuando la fuente no tiene un valor para una fecha, la interfaz indica que no está disponible.
- El panel **Contexto meteorológico 2021–2026** resume por año temperatura, humedad relativa, viento y probabilidad de precipitación. 2021–2023 provienen de los JSON de Meteomatics, con observaciones cada cinco minutos en un solo punto; 2024–2026 usan los promedios diarios ERA5-Land de cuatro localidades y la probabilidad del archivo de pronósticos históricos de Open-Meteo. Son fuentes y resoluciones distintas, así que los valores sirven como contexto y no como una serie homogénea, predicción de focos ni conteo VIIRS. La humedad de 2022–2023 corresponde a 10 m; el resto se reporta a 2 m.
- El calendario climático diario de 2021–2023 agrega las observaciones Meteomatics por fecha local en `clima_san_martin_diario_2021_2026.json`. En las fechas con cobertura VIIRS, el calendario usa la escala de detecciones; en los periodos sin cobertura VIIRS usa rangos de temperatura media diaria. Lluvia observada, humedad del suelo y CAPE no están en esos JSON y se muestran como no disponibles. Los archivos meteorológicos agregados se regeneran con `python preparar_resumen_climatico.py`.
- La tarjeta muestra precipitación acumulada en 24 horas y en 7 días (el día seleccionado y los seis anteriores). La humedad del suelo corresponde a la capa de 0–7 cm de ERA5-Land; el dato original en m³/m³ se convierte a porcentaje volumétrico y no equivale exactamente a una capa de 0–10 cm.
- Se considera **día seco** aquel cuyo promedio de precipitación es menor de 1 mm. La racha muestra cuántos días secos consecutivos hay hasta la fecha seleccionada; un día con 1 mm o más reinicia el contador. Se incluyen datos meteorológicos desde el 1 de enero de 2023 para dar contexto a las rachas de 2024.
- El **índice meteorológico experimental** suma puntos por temperatura media diaria, humedad relativa media, velocidad media del viento a 10 m y precipitación de las últimas 24 horas. Los cortes reproducen la propuesta: temperatura `<25 °C: 0`, `25–<30: 10`, `30–35: 20`, `>35: 30`; humedad `>70 %: 0`, `50–70: 10`, `30–<50: 20`, `<30: 30`; viento `<10 km/h: 0`, `10–<20: 10`, `20–30: 20`, `>30: 30`; lluvia `>20 mm: 0`, `10–20: 5`, `5–<10: 10`, `<5: 20`. La puntuación bruta se limita a 100 porque los máximos de los componentes suman 110. Clasificación: 0–25 bajo, 26–50 moderado, 51–75 alto y 76–100 extremo. La lluvia de 7 días, humedad del suelo y CAPE son información de contexto y no suman al índice.
- El índice es una comparación meteorológica histórica y regional, no una alerta oficial ni una predicción de propagación. No se calcula por píxel, no cambia al dibujar un área y no implica que exista un foco cercano a 5 km. La presencia de puntos de calor se informa por separado a partir de las detecciones VIIRS y de los filtros activos.
- El gráfico compara el promedio diario de detecciones de cada mes entre 2021 y 2026. En 2022 el promedio se calcula solo con los días cubiertos por la fuente, y los meses sin cobertura aparecen sin datos. Se actualiza al cambiar el polígono o el nivel de confianza; el calendario y el mapa responden además a los filtros de año, mes y día.
- La sección **Escenario de referencia 2027–2029** muestra una proyección exploratoria: promedia las detecciones anuales de 2025 y 2026, anualizando 2026 a partir de sus registros del 1 de enero al 5 de noviembre. Repite ese promedio como referencia constante para los tres años; el rango mostrado solo abarca esos dos valores y no es un intervalo de confianza. Se actualiza con el área y la confianza seleccionadas. La serie reciente es corta y no permite una predicción validada; la proyección no representa incendios confirmados ni una alerta oficial.
- Se marca como **actividad elevada** el mes completo de 2026 cuyo promedio diario sea al menos 50 % mayor que el promedio del mismo mes en 2024 y 2025. Es un criterio descriptivo de comparación, no una alerta oficial ni una explicación meteorológica.
- Noviembre de 2026 está incompleto: las detecciones regionales llegan al día 5 y los archivos fuente al día 7. No se incluye en el cálculo de meses destacados.

## Cobertura de los datos

- **2021:** 10.266 detecciones de Suomi-NPP, con archivo anual del 1 de enero al 31 de diciembre.
- **2022:** 394 detecciones de Suomi-NPP en los periodos disponibles del 1–6 y 15–19 de enero. Los CSV A y D eran duplicados exactos, al igual que B y C; se incluyó una copia de cada par. El resto del año no tiene cobertura en estos archivos.
- **2023:** 22.049 detecciones: Suomi-NPP: 11.701 y NOAA-21: 10.348. Suomi-NPP cubre el año; el archivo NOAA-21 está disponible del 1 de marzo al 31 de diciembre.
- **2024:** 40.482 detecciones dentro de San Martín, del 2 de enero al 30 de diciembre; NOAA-20: 13.815, NOAA-21: 13.822 y Suomi-NPP: 12.845.
- **2025:** 23.273 detecciones dentro de San Martín, del 1 de enero al 31 de diciembre; NOAA-20: 7.650, NOAA-21: 7.814 y Suomi-NPP: 7.809.
- **2026:** 13.611 detecciones dentro de San Martín, del 1 de enero al 5 de noviembre; NOAA-21: 6.802 y Suomi-NPP: 6.809. Los archivos fuente llegan hasta el 7 de noviembre; no hubo detecciones regionales el 6 y 7 de noviembre. Incluye datos de archivo hasta julio y datos near-real-time después de ese periodo, que pueden ser revisados por NASA FIRMS.

Los conteos son detecciones satelitales, no incendios únicos confirmados. Un mismo foco puede ser detectado más de una vez o por varios satélites; no se deduplicaron observaciones entre sensores. Los años 2022 y 2026 tienen cobertura parcial, por lo que sus totales no son directamente comparables con años completos.

## Detalles de los marcadores

Los registros muestran fecha, hora disponible, coordenadas, FRP, confianza VIIRS y satélite. Cuando la fuente contiene esa información, el punto muestra la provincia y la localidad poblada más cercana, junto con su distancia aproximada. La localidad es una referencia geográfica, no necesariamente el lugar exacto de la detección. Hay nombres para 1.331 registros de 2024, incorporados al coincidir exactamente fecha y coordenadas con puntos previamente identificados, y para 7.650 registros NOAA-20 de 2025. Los CSV de 2026 no incluyen localidades. En los demás casos, el popup indica que el nombre no está disponible en los datos.

## Fuentes

- [NASA FIRMS — datos VIIRS](https://firms.modaps.eosdis.nasa.gov/download/) (NOAA-20, NOAA-21 y Suomi-NPP).
- Archivos CSV FIRMS publicados en el repositorio y conjunto regional consolidado en `datos_viirs_san_martin_2021_2026.json`. El generador `preparar_dataset_viirs_historico.py` procesa los CSV de 2021–2023 en streaming, conserva las detecciones 2024–2026 y aplica el límite departamental incluido en `incendios.html`. Para regenerarlo se necesitan esos CSV fuente junto al HTML y al conjunto anterior `datos_viirs_san_martin_2024_2026.json`.
- [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api) (reanálisis ERA5-Land de temperatura y precipitación) y [Historical Forecast API](https://open-meteo.com/en/docs/historical-forecast-api) (probabilidad de precipitación de pronósticos archivados). Los valores diarios promedian cuatro localidades de referencia.
- Datos meteorológicos procesados en `clima_san_martin_diario_2024_2026.json`, con fechas visibles del 1 de enero de 2024 al 7 de noviembre de 2026 y contexto previo desde el 1 de enero de 2023. La probabilidad histórica está disponible para 248 de 366 días de 2024, los 365 días de 2025 y los 311 días disponibles de 2026; las fechas restantes se indican como no disponibles.
- [geoBoundaries — límites provinciales del Perú](https://github.com/wmgeolab/geoBoundaries/tree/9469f09/releaseData/gbOpen/PER/ADM2).
- [GeoNames — referencia geográfica de localidades](https://www.geonames.org/).
- [OpenStreetMap — nombres geográficos y atribución](https://www.openstreetmap.org/copyright), consultados para la ubicación seleccionada.
