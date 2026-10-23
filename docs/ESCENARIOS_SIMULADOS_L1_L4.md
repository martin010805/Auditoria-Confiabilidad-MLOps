# Escenario reproducible L1–L4 — datos simulados

**Importante:** el ZIP original no contiene los lotes históricos L1–L4 ni etiquetas de producción. Para completar el análisis cuantitativo del método, se generó un conjunto de datos sintético de 2.000 filas, 500 por lote, con semilla fija `20261023`. Estos resultados sirven para demostrar cálculo y decisiones SLO; no son evidencia histórica ni deben describirse como mediciones reales del sistema.

## Cómo reproducir

El archivo `evidencias/auditoria/lotes_L1_L4_simulados.csv` contiene etiquetas, score positivo, predicción a umbral 0,5, latencia y estado HTTP. Cada fila incluye `data_origin=SIMULATED_NOT_PRODUCTION`. El resumen está en `evidencias/auditoria/resumen_L1_L4_simulado.csv`.

## Lectura

- Disponibilidad se calcula como `(solicitudes - HTTP 5xx) / solicitudes`.
- Latencia se evalúa con p95 ≤ 500 ms.
- Calidad se calcula con AUC-PR, que requiere etiquetas `y_true`.
- Una ventana sin etiquetas suficientes debe quedar como “sin evidencia”, no como PASS.

Los lotes sintéticos incluyen una degradación progresiva para mostrar cómo un monitoreo podría detectar cambios. Sustituir estos datos por L1–L4 originales antes de afirmar comportamiento real.
