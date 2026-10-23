# Cómo terminar y entregar esta auditoría

## Lo que incluye este paquete
- `docs/INFORME_AUDITORIA.pdf`: informe base en PDF.
- `docs/INFORME_AUDITORIA.md`: fuente editable del informe.
- `docs/FICHAS.md`: nueve fichas con referencias verificadas al ZIP entregado.
- `monitoring/sre_alert_policy.py` y `tests/test_sre_alert_policy.py`: cambio de política de alertas y cinco pruebas unitarias que pasan.
- `tests/stress_test_plan.py`: script de carga HTTP; necesita la API funcionando y genera resultados al ejecutarse.
- `evidencias/auditoria/`: observaciones de auditoría y resultados de pruebas unitarias.

## Limitaciones que no se deben ocultar
1. El ZIP original no incluye `.git`, `mlflow.db`, `mlruns/`, el dataset `data/creditcard.csv`, lotes L0–L4 ni una implementación de detector PSI/rollback. Por eso no es posible demostrar métricas reales de producción L1–L4 ni recuperar un historial de commits anterior.
2. El incidente de Docker está basado en tu recuerdo general y en un defecto reproducible del paquete entregado: `Dockerfile` copia `mlflow.db` y `mlruns/`, pero ambos están excluidos por `.gitignore` y no aparecen en el ZIP. La hora y duración exactas no están registradas; no se inventaron.
3. Las metas SLO del informe son propuestas de diseño. La disponibilidad, latencia y calidad real por lote no se pueden calcular con los registros disponibles. `training/real_results.json` sí conserva AUC-PR de prueba temporal = 0,3005, ROC-AUC = 0,7495 y recall de clase minoritaria = 0,50, pero es evaluación de holdout, no calidad de producción L1–L4.
4. La política PSI añadida es un cambio real de código, pero no está conectada a un detector PSI que no aparece en el ZIP. No se afirma lo contrario.
5. La guía original de auditoría exige que `fichas.md` tenga historial diario en el repositorio. El ZIP de proyecto no contiene `.git`, por lo que ese historial no se puede reconstruir de forma honesta.

## Pasos para fortalecer antes de enviar
1. Ejecuta la prueba de estrés con el servicio disponible: `python tests/stress_test_plan.py`; guarda la salida JSON en `evidencias/auditoria/stress_test.json`.
2. Confirma, si puedes, el error concreto de Docker y si el problema se resolvió incluyendo/generando `mlflow.db` y `mlruns/`. Ajusta la cronología del postmortem con lo que recuerdes.
3. Si conservas el directorio original completo, con `mlflow.db`, `mlruns`, datos y `.git`, reemplaza este paquete parcial por una auditoría de ese directorio. No subas datos sensibles ni credenciales.
4. Revisa el texto y adapta la redacción a tu voz antes de entregar.
