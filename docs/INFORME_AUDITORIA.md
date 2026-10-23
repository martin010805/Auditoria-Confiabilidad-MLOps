# Informe de Auditoría de Confiabilidad — MLOps Variante B

**Fecha:** 23 de octubre de 2026. Informe completo en `INFORME_AUDITORIA.pdf` (25 páginas). Las nueve fichas también se encuentran en `FICHAS.md`.

## Resumen ejecutivo
La auditoría se basa en el ZIP del proyecto MLOps de la semana anterior. El paquete incluye FastAPI, entrenamiento con MLflow, registro CSV y evidencia de una prueba de API. El hallazgo concreto es que `Dockerfile` copia `mlflow.db` y `mlruns/` (líneas 8–10), pero ambos están excluidos por `.gitignore` y no están dentro del ZIP. Esto puede explicar los fallos de construcción de Docker que el estudiante recuerda, aunque no demuestra que fuera la única causa histórica.

## SLI/SLO propuestos
- **Disponibilidad:** 99,5% de solicitudes válidas sin respuesta 5xx durante 30 días; presupuesto propuesto: 216 minutos.
- **Latencia:** p95 ≤ 500 ms para `/predict`, objetivo 99% en una ventana móvil de 7 días; en 10.000 solicitudes el presupuesto sería 100 solicitudes fuera de objetivo.
- **Calidad:** AUC-PR ≥ 0,30 en al menos 95% de las ventanas semanales etiquetadas, con muestra mínima. La evaluación guardada en `training/real_results.json` tiene AUC-PR 0,3005, pero es un holdout temporal, no medición de producción L1–L4.

No es posible calcular los SLI reales de L1–L4 con el ZIP recibido: no hay lotes L0–L4 ni etiquetas reales por predicción; la latencia tampoco se registra. `monitoring/prediction_log.csv` contiene ocho eventos.

## Alertas
No se encontró detector PSI conectado en el paquete. Se añadió `monitoring/sre_alert_policy.py`, que agrega PSI por lote y clasifica `record`, `ticket` o `alert`. Dos o más variables severas (PSI ≥ 0,25) escalan a alerta; señales moderadas generan ticket. Se validan valores PSI negativos o no finitos. El cambio se encuentra en el commit local `e2ccd22`; se ejecutaron siete pruebas unitarias con éxito. Este commit se creó tras inicializar un historial local desde el ZIP, no es el historial remoto original.

## Postmortem
El estudiante recuerda fallos de Docker y archivos/imagen que no parecían actualizarse. La hipótesis técnica más concreta respaldada por el ZIP es que el Dockerfile depende de `mlflow.db` y `mlruns/`, artefactos no incluidos en el paquete. La hora y duración exactas no están registradas; no se inventan. Para confirmar la causa histórica harían falta logs originales de build/arranque.

## Toil, cascada y estrés
Se inventariaron comandos manuales del README y se priorizó automatizar build, pruebas y chequeo de salud. Los tiempos de toil son estimaciones de planificación, no registros históricos; por eso no se afirma un porcentaje real de seis meses. No se encontró watcher de rollback ni detector PSI, así que el escenario adverso se documenta como prueba de diseño futura, no como fallo ejecutado de un componente inexistente. `tests/stress_test_plan.py` prepara una prueba HTTP de 200 solicitudes y 25 trabajadores; requiere una API que arranque con un modelo accesible y aún no tiene resultados de carga.

## Limitaciones y próximos pasos
1. Recuperar, si existe, el directorio completo con `.git`, `mlflow.db`, `mlruns/`, dataset y lotes L0–L4.
2. Registrar latencia, estado HTTP, versión del modelo, batch ID y etiqueta real.
3. Conectar la política de alertas a un detector PSI real.
4. Ejecutar el script de estrés y guardar su salida JSON.
5. Confirmar la cronología del problema de Docker si se recuerdan más detalles.

El informe completo, con tablas, análisis y nueve fichas en tres puntos, está en `INFORME_AUDITORIA.pdf` y `FICHAS.md`.
