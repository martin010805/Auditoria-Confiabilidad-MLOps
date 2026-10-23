# Postmortem — fallo de Docker (reconstrucción aproximada)

**Tipo de evidencia:** recuerdo del operador + hallazgo estático del ZIP. No es un registro contemporáneo ni una cronología verificada.

## Resumen en tres líneas
El viernes 16 de octubre de 2026, durante el trabajo del proyecto anterior, Docker presentó problemas de arranque y el comportamiento de archivos/imagen parecía no reflejar los cambios recientes. El recuerdo sitúa el problema aproximadamente entre las 16:00 y las 21:00, con el episodio más claro alrededor de las 19:30–20:30. En la auditoría posterior se encontró una causa técnica plausible: el Dockerfile copia `mlflow.db` y `mlruns/`, ausentes del ZIP y excluidos por `.gitignore`; no hay logs originales para confirmar que esta fuera la causa única.

## Cronología reconstruida (horas aproximadas, no verificadas)
| Hora estimada | Evento | Base de la afirmación |
|---|---|---|
| 16:00–19:00 | Trabajo sobre el proyecto y preparación/ejecución del entorno. | Ventana general recordada por el estudiante; sin logs. |
| ~19:30 | Se observa que Docker no arranca correctamente o que los cambios no parecen reflejarse. | Recuerdo aproximado del estudiante. |
| ~20:00 | Se intenta revisar/volver a ejecutar el contenedor o la imagen. | Reconstrucción tentativa; no hay consola guardada. |
| ~20:30 | El problema sigue sin quedar documentado como resuelto. | Recuerdo aproximado; resultado final no verificable. |
| Auditoría del 23-oct | Se inspecciona `Dockerfile` líneas 8–10: intenta copiar `mlflow.db` y `mlruns/`, que no venían en el ZIP. | Hallazgo estático verificable del paquete recibido. |

## Causa probable y brecha de detección
La hipótesis técnica principal es un build no reproducible por depender de artefactos locales que no se incluyen ni se generan explícitamente. También es posible que hubiese caché de Docker o rutas/volúmenes desactualizados, pero no hay evidencia suficiente para atribuirlo. La brecha fue no guardar `docker compose build --no-cache`, `docker compose up`, estado de contenedores y hashes de imagen.

## Acciones correctivas
1. Corregir Dockerfile para que los artefactos se generen o descarguen en una etapa reproducible; responsable: mantenedor del proyecto; plazo: próxima iteración.
2. Añadir build limpio en CI; responsable: mantenedor; plazo: antes del próximo despliegue.
3. Guardar logs de build/arranque, versión de imagen y resultado de `/health`; responsable: operador; plazo: inmediato.

## Qué salió bien
El proyecto conserva README y endpoint `/health`; existe evidencia de una prueba API exitosa en una ejecución puntual.

**Nota para entrega:** conservar la palabra “aproximada” y no convertir esta reconstrucción en un log histórico. Si el estudiante recuerda con más certeza la hora o la resolución, actualizar antes de entregar.
