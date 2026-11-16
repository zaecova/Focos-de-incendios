# Documentación del calendario armonizado de focos de calor

## Propósito

Este proyecto organiza detecciones de focos MODIS y VIIRS en una estructura común para San Martín entre 2021 y 2026. Permite filtrar por sensor y rango de fechas, dibujar un área, analizar y descargar registros y visualizaciones. La estructura común facilita comparar la actividad por sensor, pero no calibra diferencias de sensibilidad, tamaño de píxel ni frecuencia de observación. Las detecciones son focos de calor, no incendios confirmados.

## Uso del mapa

1. Arrastra el mapa para desplazarte y usa los controles **+** y **−** para acercar o alejar.
2. Abre **Capas** para activar o desactivar las detecciones, las capas de densidad y el límite departamental de San Martín.
3. Usa los filtros de año, mes, sensor y confianza. Los controles **Desde** y **Hasta** admiten un intervalo personalizado; al usarlos, el mapa, el calendario y la serie mensual se filtran por esas fechas. El selector de sensor permite comparar VIIRS, ver ambos sensores o elegir MODIS por año (2021–2026); al elegir MODIS, el filtro de año y el calendario se ajustan al año elegido para mostrar solo sus detecciones. Las fechas **Desde** y **Hasta** se limitan a ese año; si **Año** está en **Todos**, la primera fecha seleccionada fija el año para ambas.
4. Pulsa **Dibujar área en el mapa**, traza un polígono y cierra su contorno para limitar los resultados a esa zona. **Quitar área** restaura toda la región.
5. El calendario muestra la intensidad diaria; pulsa una fecha para filtrar el mapa por ese día y consultar detecciones, temperatura, probabilidad histórica de precipitación y días secos. **Quitar día** vuelve al intervalo elegido.
6. Pasa el cursor sobre un marcador con nombre para ver la localidad cercana; selecciónalo para consultar todos sus detalles.

## Capas y leyenda

- **Puntos MODIS + VIIRS · FRP (MW):** paleta azul, ámbar y magenta para los rangos hasta 20 MW, más de 20 y hasta 50 MW, y más de 50 MW. El tamaño también aumenta por rango. El popup indica sensor y confianza; MODIS conserva además su confianza numérica.
- Los puntos son focos de calor detectados por satélite, no incendios confirmados. GEOPERÚ ofrece alertas oficiales georreferenciadas, pero esa capa operativa no constituye un historial de incendios ocurridos: https://visor.geoperu.gob.pe/?layers=40031
- Los archivos MODIS usados son FIRMS C6.1 estándar y NRT de 2021–2026. Se retienen puntos dentro de San Martín, con tipo 0 (presunto fuego de vegetación) cuando el archivo incluye el campo `type`, y se quitan duplicados exactos entre archivos. La clase de confianza se normaliza a baja/nominal/alta y se conserva el puntaje MODIS de 0 a 100. Se conserva el sensor de origen y no se eliminan detecciones coincidentes entre MODIS y VIIRS.
- La normalización de formato no es una calibración intersensor. Las series y comparaciones de tendencia deben filtrarse por sensor; el aviso comparativo y la proyección se desactivan al seleccionar ambos sensores.
- Los controles **Desde** y **Hasta** limitan el mapa, los conteos y la serie mensual. **Descargar detecciones CSV** exporta los puntos filtrados; **Descargar resumen CSV** exporta el recuento y ámbito; **Descargar gráfico PNG** guarda la visualización mensual.
- **Detecciones 2021:** archivo anual de Suomi-NPP.
- **Detecciones 2022:** 394 detecciones de Suomi-NPP en las fechas disponibles del archivo: 1–6 y 15–19 de enero. No se debe interpretar el resto del año como cobertura sin focos.
- **Detecciones 2023:** archivos anuales disponibles de Suomi-NPP y NOAA-21.
- **Detecciones 2024–2025:** NOAA-20, NOAA-21 y Suomi-NPP.
- **Detecciones 2026:** NOAA-21 y Suomi-NPP (VIIRS), más 698 detecciones MODIS Terra/Aqua dentro de San Martín en 96 fechas. Archivos MODIS disponibles del 1 de enero al 15 de noviembre de 2026; datos VIIRS regionales hasta el 5 de noviembre y fuente hasta el 7 de noviembre.
- El mapa presenta el total de registros disponibles por año. Una detección no equivale a un incendio único y satélites distintos pueden observar el mismo foco.
- **Mancha de calor:** muestra la concentración de detecciones de la capa correspondiente; no representa una probabilidad de incendio.
- **Límite departamental:** al seleccionar una zona del mapa se consulta el nombre geográfico cercano mediante OpenStreetMap; el popup también muestra la provincia, departamento y coordenadas. El nombre es una referencia aproximada y requiere conexión a internet.

## Calendario y patrones históricos

- El panel **Resumen de actividad** usa el año seleccionado y las fechas con cobertura del sensor. Compara el promedio diario con las mismas fechas de otros años que tengan datos del mismo sensor; MODIS y VIIRS se comparan por separado. Al seleccionar ambos sensores o usar fechas personalizadas, muestra un resumen sin alerta comparativa para evitar conclusiones sesgadas.
- El panel muestra un aviso experimental cuando el intervalo tiene al menos cinco detecciones y su promedio diario es al menos 50 % mayor que la referencia disponible. Las notificaciones emergentes se reservan para el año más reciente; al explorar años anteriores, el panel solo presenta la comparación histórica. No vigila datos en vivo, no predice incendios, no descarta peligro cuando no se activa y no es una alerta oficial. Los datos VIIRS son detecciones satelitales, no incendios confirmados.
- El calendario interactivo resume los focos del sensor seleccionado por día y admite selección directa de una fecha. En fechas cubiertas sin registros regionales, el calendario indica cero detecciones; en fechas sin cobertura muestra temperatura si hay datos meteorológicos.
- Al seleccionar un día, el calendario muestra el total de focos del sensor seleccionado, la temperatura media/máxima/mínima, la precipitación diaria, la probabilidad histórica de precipitación cuando está disponible y la racha consecutiva de días secos. El conteo respeta área, sensor y confianza; el clima siempre representa el promedio regional de San Martín.
- El promedio meteorológico simple usa cuatro localidades de referencia: Moyobamba, Tarapoto, Juanjuí y Tocache. Temperatura, humedad relativa, viento, precipitación diaria y humedad del suelo provienen del reanálisis ERA5-Land de Open-Meteo. La probabilidad es el promedio de `precipitation_probability_max` en el archivo de pronósticos históricos de Open-Meteo; no es una probabilidad actual ni se infiere de la lluvia observada. CAPE también procede del archivo de pronósticos históricos. Cuando la fuente no tiene un valor para una fecha, la interfaz indica que no está disponible.
- El panel **Contexto meteorológico 2021–2026** resume por año temperatura, humedad relativa, viento y probabilidad de precipitación. 2021–2023 provienen de los JSON de Meteomatics, con observaciones cada cinco minutos en un solo punto; 2024–2026 usan los promedios diarios ERA5-Land de cuatro localidades y la probabilidad del archivo de pronósticos históricos de Open-Meteo. Son fuentes y resoluciones distintas, así que los valores sirven como contexto y no como una serie homogénea, predicción de focos ni conteo VIIRS. La humedad de 2022–2023 corresponde a 10 m; el resto se reporta a 2 m.
- El calendario climático diario de 2021–2023 agrega las observaciones Meteomatics por fecha local en `clima_san_martin_diario_2021_2026.json`. En las fechas con cobertura VIIRS, el calendario usa la escala de detecciones; en los periodos sin cobertura VIIRS usa rangos de temperatura media diaria. Lluvia observada, humedad del suelo y CAPE no están en esos JSON y se muestran como no disponibles. Los archivos meteorológicos agregados se regeneran con `python preparar_resumen_climatico.py`.
- La tarjeta muestra precipitación acumulada en 24 horas y en 7 días (el día seleccionado y los seis anteriores). La humedad del suelo corresponde a la capa de 0–7 cm de ERA5-Land; el dato original en m³/m³ se convierte a porcentaje volumétrico y no equivale exactamente a una capa de 0–10 cm.
- Se considera **día seco** aquel cuyo promedio de precipitación es menor de 1 mm. La racha muestra cuántos días secos consecutivos hay hasta la fecha seleccionada; un día con 1 mm o más reinicia el contador. Se incluyen datos meteorológicos desde el 1 de enero de 2023 para dar contexto a las rachas de 2024.
- El **índice meteorológico experimental** suma puntos por temperatura media diaria, humedad relativa media, velocidad media del viento a 10 m y precipitación de las últimas 24 horas. Los cortes reproducen la propuesta: temperatura `<25 °C: 0`, `25–<30: 10`, `30–35: 20`, `>35: 30`; humedad `>70 %: 0`, `50–70: 10`, `30–<50: 20`, `<30: 30`; viento `<10 km/h: 0`, `10–<20: 10`, `20–30: 20`, `>30: 30`; lluvia `>20 mm: 0`, `10–20: 5`, `5–<10: 10`, `<5: 20`. La puntuación bruta se limita a 100 porque los máximos de los componentes suman 110. Clasificación: 0–25 bajo, 26–50 moderado, 51–75 alto y 76–100 extremo. La lluvia de 7 días, humedad del suelo y CAPE son información de contexto y no suman al índice.
- El índice es una comparación meteorológica histórica y regional, no una alerta oficial ni una predicción de propagación. No se calcula por píxel, no cambia al dibujar un área y no implica que exista un foco cercano a 5 km. La presencia de puntos de calor se informa por separado a partir de las detecciones VIIRS y de los filtros activos.
- El gráfico compara focos por día de cada mes y se actualiza con el sensor, intervalo, área y confianza seleccionados. Las curvas MODIS y VIIRS se calculan por separado; la línea combinada se ofrece como recuento descriptivo, no como comparación calibrada.
- La sección **Escenario de referencia 2027–2029** muestra una proyección exploratoria basada solo en VIIRS de 2025 y 2026. No se calcula para MODIS, el total combinado ni un intervalo personalizado. La serie reciente es corta y no permite una predicción validada; la proyección no representa incendios confirmados ni una alerta oficial.
- Se marca como **actividad elevada** el mes completo de 2026 cuyo promedio diario sea al menos 50 % mayor que el promedio del mismo mes en 2024 y 2025. Es un criterio descriptivo de comparación, no una alerta oficial ni una explicación meteorológica.
- Noviembre de 2026 está incompleto y sus datos de archivo/NRT tienen fechas distintas por sensor; no se trata como mes completo para anomalías.

## Cobertura de los datos

- **2021:** VIIRS registra 10.266 detecciones de Suomi-NPP y MODIS 1.920.
- **2022:** VIIRS registra 394 detecciones en los periodos del 1–6 y 15–19 de enero; MODIS registra 2.396.
- **2023:** VIIRS registra 22.049 detecciones y MODIS 1.897.
- **2024:** VIIRS registra 40.482 detecciones y MODIS 2.474.
- **2025:** VIIRS registra 23.273 detecciones y MODIS 915.
- **2026:** VIIRS registra 13.611 detecciones (6.802 NOAA-21 y 6.809 Suomi-NPP) y MODIS 698. La cobertura VIIRS regional llega al 5 de noviembre; el archivo fuente llega al 7. MODIS combina archivo estándar hasta agosto y NRT posterior, disponible hasta el 15 de noviembre; NASA FIRMS puede revisar datos NRT.

Los conteos son detecciones satelitales, no incendios únicos confirmados. Un mismo foco puede ser detectado más de una vez o por varios satélites; no se deduplicaron observaciones entre sensores. MODIS y VIIRS tienen sensibilidad, resolución y frecuencia distintas; el esquema común no calibra esa diferencia. Los años 2022 y 2026 tienen cobertura parcial, por lo que sus totales no son directamente comparables con años completos.

## Detalles de los marcadores

Los registros muestran fecha, hora UTC, coordenadas, FRP, confianza, sensor y satélite. Cuando la fuente contiene esa información, el punto muestra la provincia y la localidad poblada más cercana, junto con su distancia aproximada. La localidad es una referencia geográfica, no necesariamente el lugar exacto de la detección. Hay nombres para 1.331 registros de 2024, incorporados al coincidir exactamente fecha y coordenadas con puntos previamente identificados, y para 7.650 registros NOAA-20 de 2025. Los registros MODIS aún no incluyen localidades.

## Fuentes

- [NASA FIRMS — datos VIIRS](https://firms.modaps.eosdis.nasa.gov/download/) (NOAA-20, NOAA-21 y Suomi-NPP) y [datos MODIS](https://firms.modaps.eosdis.nasa.gov/content/descriptions/FIRMS_MODIS_Firehotspots.html) (Terra y Aqua).
- El archivo consolidado de la aplicación es `datos_focos_harmonizados_2021_2026.json`. Para regenerarlo, agrega los CSV o ZIP MODIS FIRMS C6.1 a `MODIS/` y ejecuta `python preparar_dataset_harmonizado.py`. El proceso incorpora la serie VIIRS regional existente, recorta MODIS a San Martín, normaliza los campos y la confianza, y conserva el sensor para análisis.
- Los umbrales de clase MODIS siguen la guía NASA: baja <30, nominal 30–<80 y alta ≥80. [Guía de usuario MODIS C6/C6.1](https://www.earthdata.nasa.gov/s3fs-public/2023-09/MODIS_C6_C6.1_Fire_User_Guide_1.0.pdf).
- Los datos históricos VIIRS se mantienen en `datos_viirs_san_martin_2021_2026.json`; el generador `preparar_dataset_viirs_historico.py` prepara esa serie. `preparar_dataset_harmonizado.py` construye el archivo que consume la web.
- [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api) (reanálisis ERA5-Land de temperatura y precipitación) y [Historical Forecast API](https://open-meteo.com/en/docs/historical-forecast-api) (probabilidad de precipitación de pronósticos archivados). Los valores diarios promedian cuatro localidades de referencia.
- Datos meteorológicos procesados en `clima_san_martin_diario_2024_2026.json`, con fechas visibles del 1 de enero de 2024 al 7 de noviembre de 2026 y contexto previo desde el 1 de enero de 2023. La probabilidad histórica está disponible para 248 de 366 días de 2024, los 365 días de 2025 y los 311 días disponibles de 2026; las fechas restantes se indican como no disponibles.
- [geoBoundaries — límites provinciales del Perú](https://github.com/wmgeolab/geoBoundaries/tree/9469f09/releaseData/gbOpen/PER/ADM2).
- [GeoNames — referencia geográfica de localidades](https://www.geonames.org/).
- [OpenStreetMap — nombres geográficos y atribución](https://www.openstreetmap.org/copyright), consultados para la ubicación seleccionada.

