# Informe de Auditoría de Confiabilidad — MLOps Variante B

**Fecha:** 23 de octubre de 2026. El informe principal está en `Martin_AuditoriaConfiabilidad.pdf`; las nueve fichas están en `fichas.md` y `docs/FICHAS.md`.

## Resumen ejecutivo
La auditoría se basa en el ZIP del proyecto MLOps de la semana anterior. El proyecto incluye FastAPI, registro CSV, entrenamiento con MLflow y evidencia de una prueba de API. El hallazgo verificable es que `Dockerfile` copia `mlflow.db` y `mlruns/` (líneas 8–10), pero no estaban en el ZIP y están excluidos por `.gitignore`. Esto puede explicar el problema de Docker que recuerda el estudiante, aunque no prueba que fuera la causa única.

## SLI/SLO propuestos
- **Disponibilidad:** 99,5% de solicitudes válidas sin respuesta 5xx durante 30 días; presupuesto de 216 minutos.
- **Latencia:** p95 ≤ 500 ms para `/predict`; objetivo de 99% de solicitudes dentro del umbral en una ventana móvil de 7 días.
- **Calidad:** AUC-PR ≥ 0,30 en ventanas etiquetadas. El holdout guardado en `training/real_results.json` da AUC-PR 0,3005, no una medición de producción.

## Lotes L1–L4
El ZIP original no contenía los lotes históricos ni etiquetas de producción. Para completar el ejercicio de cálculo, se creó un dataset sintético de 2.000 filas (500 por lote) con semilla fija. `evidencias/auditoria/lotes_L1_L4_simulados.csv` contiene los registros y `resumen_L1_L4_simulado.csv` sus métricas. Todos los registros están marcados `SIMULATED_NOT_PRODUCTION`; no deben presentarse como resultados históricos. En el escenario sintético L1 cumple los tres objetivos; L2 falla AUC-PR; L3 falla latencia y AUC-PR; L4 falla disponibilidad, latencia y AUC-PR.

## Alertas y código
No se encontró detector PSI conectado en el paquete. Se añadió `monitoring/sre_alert_policy.py`, que clasifica señales por lote como `record`, `ticket` o `alert`. Las siete pruebas unitarias pasan (`python -m pytest -q tests/test_sre_alert_policy.py` → 7 passed). El cambio es real, pero la política todavía debe conectarse a un detector PSI operativo.

## Postmortem de Docker
El recuerdo sitúa el trabajo del viernes 16 de octubre aproximadamente entre 16:00 y 21:00, con el episodio más claro alrededor de 19:30–20:30. La cronología está etiquetada como reconstrucción aproximada, no como log contemporáneo. El `Dockerfile` copia artefactos que no estaban en el ZIP, lo que es una causa probable. La hora exacta, duración y resolución histórica no se pueden confirmar sin logs.

## Prueba de carga
Se ejecutó `tests/stress_test_stub.py` sobre la ruta FastAPI con un modelo determinista de prueba: 200 respuestas HTTP 200, 0 errores, 0,539 segundos, 370,81 solicitudes/s y p95 99,15 ms. Es una prueba real de la ruta en `TestClient`, pero usa un modelo simulado, sin red ni contenedor; no equivale a una prueba de rendimiento con el modelo MLflow real. El test de extremo a extremo sigue disponible en `tests/stress_test_plan.py` para cuando se recuperen los artefactos.

## Toil, rollback y limitaciones
Las horas de toil son estimaciones de planificación, no registros reales de seis meses. No se encontró un watcher de rollback automático, por lo que el escenario adversarial se especifica como plan de prueba, no como incidente ejecutado. El paquete original tampoco incluye `.git`, `mlflow.db`, `mlruns/`, el dataset ni los lotes históricos. Los commits disponibles pertenecen a un historial local creado durante esta auditoría, no al historial original del estudiante.
