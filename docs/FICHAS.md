# Fichas de lectura — Auditoría de Confiabilidad (Variante B)

> **Nota de honestidad documental:** las referencias de archivo y línea se verificaron sobre el ZIP entregado para esta auditoría. El ZIP no incluye historial `.git`, lotes L0–L4 ni detector PSI/reversión automática completos. Por eso las fichas distinguen lo implementado de lo ausente; no atribuyen al proyecto funciones que no se encontraron.

## Capítulo 3 — Embracing Risk
1. **Qué dice el capítulo.** La confiabilidad no significa eliminar todo riesgo, sino decidir cuánto riesgo es aceptable y usar un presupuesto de error para equilibrar estabilidad y cambios. Si se consume el presupuesto, la decisión debe cambiar: reducir despliegues y priorizar recuperar confiabilidad.
2. **Qué hice yo.** En el proyecto se registran métricas de evaluación y parámetros en MLflow (`training/train.py`, líneas 60–90; `training/train_real.py`, líneas 107–122). Sin embargo, no se encontró una política de presupuesto de error ni una decisión operativa basada en ese presupuesto. Las evidencias de API muestran una comprobación puntual de salud (`evidencias/health.json`, líneas 1–4), no una serie de disponibilidad.
3. **Qué cambiaría hoy.** Definiría SLO explícitos para disponibilidad, latencia y calidad, y una política que congele promociones si se agota el presupuesto. Los objetivos de este informe son propuestas de operación, no mediciones históricas.

## Capítulo 4 — Service Level Objectives
1. **Qué dice el capítulo.** Un SLI es una medida observable de lo que recibe el usuario; un SLO fija el nivel esperado durante una ventana. Debe poder calcularse con registros y relacionarse con el impacto al negocio.
2. **Qué hice yo.** `/health` devuelve `status` y `model_loaded` (`serving/app.py`, líneas 75–81); `/predict` devuelve clase y probabilidades (`serving/app.py`, líneas 83–97). `/metrics` recuenta predicciones y probabilidades, pero no registra latencia (`serving/app.py`, líneas 167–208). El CSV registra tiempo y resultado, no duración ni etiqueta real (`monitoring/logger.py`, líneas 17–30; `monitoring/prediction_log.csv`, líneas 1–9).
3. **Qué cambiaría hoy.** Añadiría latencia por petición, estado HTTP y versión del modelo; agregaría métricas con etiquetas reales cuando lleguen. No reportaría AUC-PR de producción sin etiquetas verdaderas.

## Capítulo 6 — Monitoring Distributed Systems
1. **Qué dice el capítulo.** El monitoreo útil combina métricas, registros y señales que permiten distinguir un fallo del servicio, lentitud y degradación de calidad. Las señales deben ser accionables y cubrir la experiencia observable, no solo el estado interno.
2. **Qué hice yo.** El proyecto conserva eventos de predicción en CSV (`monitoring/logger.py`, líneas 17–30) y cuenta clases y probabilidades (`serving/app.py`, líneas 167–208). La evidencia disponible contiene ocho predicciones (`evidencias/metrics.json`, líneas 1–7), pero no lotes L1–L4 ni etiquetas reales asociadas a cada predicción.
3. **Qué cambiaría hoy.** Añadiría `request_duration_ms`, `status_code`, `model_version`, `batch_id` y etiqueta real cuando esté disponible. Haría una gráfica temporal y alertas sobre ventanas, no sobre una sola petición.

## Capítulo 10 — Practical Alerting
1. **Qué dice el capítulo.** Una alerta que despierta a alguien debe requerir acción inmediata. Señales informativas o de baja urgencia deben ser tickets o registros; demasiadas notificaciones individuales crean ruido.
2. **Qué hice yo.** La API implementa `/metrics`, pero no se encontró un sistema de alertas PSI ni destinatarios en los archivos entregados (`serving/app.py`, líneas 167–208; `monitoring/logger.py`, líneas 17–30). La guía del proyecto anterior requería monitoreo de PSI, pero no se ve implementado en este ZIP.
3. **Qué cambiaría hoy.** Añadí `monitoring/sre_alert_policy.py`, que agrega señales por lote y clasifica normal/moderado/severo; sus pruebas están en `tests/test_sre_alert_policy.py`. La política es una pieza nueva y probada, pero debe conectarse al detector PSI real cuando exista.

## Capítulo 5 — Eliminating Toil
1. **Qué dice el capítulo.** Toil es trabajo operativo manual, repetitivo, automatizable, sin valor duradero y que crece con el servicio. Se debe medir y reducir, pero conservar manuales las decisiones de alto riesgo que necesitan juicio humano.
2. **Qué hice yo.** El README describe comandos manuales de instalación, entrenamiento, ejecución de API y Docker (`README.md`, líneas 6–25). `pipeline/run_pipeline.py`, líneas 9–19, solo invoca un script de entrenamiento; no orquesta etapas independientes ni reintentos.
3. **Qué cambiaría hoy.** Automatizaría primero pruebas, construcción de imagen y comprobaciones de salud. Mantendría manual la aprobación inicial de un modelo o la reactivación tras un incidente hasta tener evidencia y salvaguardas.

## Capítulo 22 — Addressing Cascading Failures
1. **Qué dice el capítulo.** Una recuperación automática puede amplificar el fallo si reacciona a señales ruidosas, usa ventanas pequeñas o desencadena ciclos de acciones. Debe limitarse la tasa de acciones, exigir señales sostenidas y probarse bajo condiciones adversas.
2. **Qué hice yo.** El servicio carga un modelo desde una ruta configurada (`serving/app.py`, líneas 20–32), pero no se encontró un vigilante de calidad que restaure la versión archivada ni una salvaguarda contra ciclos. El proyecto de la semana anterior sí define ese requisito en su guía, pero el ZIP entregado no muestra la implementación.
3. **Qué cambiaría hoy.** Antes de automatizar rollback, exigiría varias ventanas degradadas, confirmación con etiquetas, cooldown, límite de una reversión por versión y auditoría de decisión. Añadí un plan de estrés reproducible (`tests/stress_test_plan.py`); debe ejecutarse contra un servicio realmente levantado para obtener resultados.

## Capítulo 15 — Postmortem Culture
1. **Qué dice el capítulo.** El postmortem describe cómo falló el sistema y qué controles faltaron, sin culpar personas. Debe incluir impacto, cronología, causa raíz, detección, acciones con responsable/plazo y qué funcionó bien.
2. **Qué hice yo.** Recuerdo que Docker a veces no arrancaba y que la imagen o sus archivos no parecían actualizarse. El ZIP actual permite identificar una causa técnica plausible: `Dockerfile`, líneas 8–10, copia `mlflow.db` y `mlruns/`, pero esos elementos no están incluidos en el ZIP; `.gitignore` los excluye (`.gitignore`, líneas 1–6). Esto puede provocar fallo de construcción cuando se reconstruye desde ese paquete, pero no demuestra por sí solo que fuera la única causa histórica.
3. **Qué cambiaría hoy.** Dejaría de depender de artefactos ignorados que no viajan con el repositorio; usaría un proceso reproducible para inicializar MLflow/registrar modelo, una comprobación previa de los archivos requeridos y un `docker compose build --no-cache` solo cuando sea necesario. La hora y duración exactas del incidente no se conservaron; no las invento.

## Capítulo 12 — Effective Troubleshooting
1. **Qué dice el capítulo.** Resolver un fallo requiere formular hipótesis, reunir evidencia, aislar variables y cambiar una cosa a la vez. Los mensajes de error y los pasos reproducibles valen más que reiniciar repetidamente sin registrar lo ocurrido.
2. **Qué hice yo.** El README enumera comandos de entrenamiento y ejecución (`README.md`, líneas 10–19), y hay una evidencia de respuesta exitosa de API (`evidencias/api_test.json`, líneas 1–12). No se incluyeron logs del fallo de Docker ni un registro de intentos, así que la cronología histórica es incompleta.
3. **Qué cambiaría hoy.** Guardaría el texto completo del error de `docker compose build` y `docker compose up`, la salida de `docker compose config`, el estado de contenedores y los hashes de imagen antes/después. Así se puede diferenciar error de construcción, carga del modelo y puerto ocupado.

## Capítulo 17 — Testing for Reliability
1. **Qué dice el capítulo.** Las pruebas deben verificar comportamiento bajo fallos y carga, no solo que una función devuelva el resultado esperado. Conviene probar entradas inválidas, dependencias ausentes, reinicios, concurrencia y condiciones de degradación.
2. **Qué hice yo.** `tests/test_api.py`, líneas 6–37, verifica salud y una predicción cuando el servicio ya está activo; no levanta la API ni cubre estrés, entradas inválidas o ausencia del modelo. El archivo de evidencia muestra una predicción de prueba, no una prueba de carga (`evidencias/api_test.json`, líneas 1–12).
3. **Qué cambiaría hoy.** Separaría pruebas unitarias y de integración, probaría la API con dependencias controladas y ejecutaría `tests/stress_test_plan.py` contra el servicio. La prueba de estrés incluida no tiene resultados aún: debe ejecutarse en un entorno con Docker/modelo disponible y adjuntar su salida real.
