# Qué contiene la entrega

- `Martin_AuditoriaConfiabilidad.pdf`: informe principal de 25 páginas.
- `fichas.md`: nueve fichas, tres apartados por capítulo, en la raíz del proyecto como pide la guía.
- `docs/FICHAS.md`: copia de lectura de las fichas.
- `docs/POSTMORTEM_DOCKER.md`: reconstrucción aproximada del incidente recordado, con horas estimadas marcadas como no verificadas.
- `docs/ESCENARIOS_SIMULADOS_L1_L4.md`: explicación de los lotes sintéticos.
- `evidencias/auditoria/lotes_L1_L4_simulados.csv`: 2.000 filas sintéticas con etiquetas, scores, latencia y estado HTTP.
- `evidencias/auditoria/resumen_L1_L4_simulado.csv`: métricas calculadas por lote.
- `monitoring/sre_alert_policy.py` y `tests/test_sre_alert_policy.py`: política PSI añadida y siete pruebas unitarias; todas pasan.
- `tests/stress_test_stub.py`: prueba ejecutada de la ruta FastAPI con modelo determinista de prueba.
- `evidencias/auditoria/stress_test_stub.json`: salida real de esa prueba de ruta, no prueba de producción.
- `tests/stress_test_plan.py`: prueba HTTP preparada para ejecutarse con el modelo real disponible.

## Qué significan las evidencias

Los lotes L1–L4 son simulados porque el ZIP original no contenía datos históricos ni etiquetas de producción. La cronología de Docker se reconstruyó a partir del recuerdo del estudiante y se etiqueta como aproximada; no es un registro de consola. La prueba de carga ejecutada usa la ruta real de FastAPI con un modelo dummy dentro de TestClient, por lo que no acredita rendimiento del modelo MLflow real ni del contenedor.

El ZIP original tampoco contenía `.git`, `mlflow.db`, `mlruns/` ni el dataset. Por eso el historial Git previo no se puede recuperar; los commits del paquete son locales y posteriores a la recepción del ZIP. No se debe presentar lo simulado como evidencia histórica.

## Pruebas ejecutadas

- `python -m pytest -q tests/test_sre_alert_policy.py` → 7 passed.
- `python tests/stress_test_stub.py` → 200 respuestas HTTP 200, 0 errores, 370,81 solicitudes/s, p95 99,15 ms; modelo dummy y TestClient.
