# Entrenamiento experimental paralelo

El servicio `training` instala StatsForecast y AutoGluon TimeSeries con PyTorch CPU,
en una imagen distinta de la API. No necesita Python instalado en Windows.

Desde `sistema-web-agro`:

```powershell
docker compose up -d --build --wait training backend frontend
docker compose exec training pip check
docker compose exec training python -m unittest test_protocol
```

En Pronósticos, la opción **Entrenamiento paralelo experimental** está marcada por
 defecto. Iniciar requiere rol ADMIN. Ejecuta dos procesos simultáneos, uno por
biblioteca; desmarcarla permite la ejecución secuencial. Solo una ejecución activa
por servicio. Contenedor limitado a dos CPU y 4 GB, con hilos numéricos limitados.

El experimento selecciona la última secuencia semanal continua de desarrollo
hasta el 20 de abril de 2026, sin atravesar huecos ni rellenarlos con ceros. Reserva
las últimas 1, 2 o 4 semanas para un único bloque externo de validación; ambas
bibliotecas reciben exactamente el mismo entrenamiento y contraste. AutoGluon usa
además validación interna temporal para seleccionar/combinar modelos. Esta prueba
acotada verifica el flujo; no sustituye validación temporal con varias ventanas,
no modifica los resultados del piloto y no ejecuta la prueba final.

StatsForecast: AutoETS y AutoARIMA sin estacionalidad anual, más Naive. AutoGluon:
ETS y DirectTabular con GBM, máximo 50 iteraciones y rezagos 1,2,3,4,8,12; ensamble
si hay modelos suficientes. Sin pesos remotos, APIs de pago ni modelos fundacionales.
Las predicciones negativas se acotan a cero. No se muestran intervalos como calibrados.

Presupuesto de ajuste AutoGluon: 30/60/180 segundos; cada proceso tiene un límite
externo adicional de 120 segundos para importar, ajustar y guardar resultados.
No es una garantía estricta de duración total. Los fallos de cada biblioteca se
informan individualmente. Una ejecución parcialmente fallida no se etiqueta como exitosa.

El volumen `training_state` conserva entradas, modelos, resultados, logs, versiones
y huellas SHA256. El archivo `/opt/training-requirements.lock` registra las versiones
resueltas. Las versiones utilizadas se pueden consultar en la vista y exportar con:

```powershell
docker compose exec -T training cat /opt/training-requirements.lock
```

La compilación instala el lock versionado con StatsForecast 2.0.3, AutoGluon
1.6.3 y PyTorch 2.13.0+cpu. Cada ejecución conserva la huella del lock, la
huella del snapshot y la revisión indicada al construir la imagen. Tras un
commit limpio, establecer la revisión antes de reconstruir el servicio.

```powershell
$env:AGRO_SOURCE_REVISION = git rev-parse HEAD
docker compose build training
docker image inspect agroscope-training:local --format '{{.Id}}'
```
