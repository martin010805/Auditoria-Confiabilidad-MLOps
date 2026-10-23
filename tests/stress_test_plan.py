"""Prueba de estrés HTTP reproducible. Requiere la API levantada en localhost:8000.
No se ejecuta automáticamente en pytest para no depender de un servicio externo.
"""
import concurrent.futures
import json
import time
import urllib.error
import urllib.request

URL = "http://127.0.0.1:8000/predict"
PAYLOAD = json.dumps({"features": [0.0] * 20}).encode("utf-8")


def one_request(_):
    req = urllib.request.Request(URL, data=PAYLOAD, headers={"Content-Type": "application/json"})
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            response.read()
            return response.status, (time.perf_counter() - start) * 1000
    except Exception:
        return 0, (time.perf_counter() - start) * 1000


def main(total=200, workers=25):
    started = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(one_request, range(total)))
    elapsed = time.perf_counter() - started
    latencies = sorted(ms for _, ms in results)
    successes = sum(status == 200 for status, _ in results)
    p95 = latencies[min(len(latencies) - 1, int(0.95 * len(latencies)))]
    print(json.dumps({
        "requests": total, "workers": workers, "successes": successes,
        "errors": total - successes, "elapsed_seconds": round(elapsed, 3),
        "requests_per_second": round(total / elapsed, 2), "p95_latency_ms": round(p95, 2),
        "note": "Ejecutar solo después de levantar la API; guardar salida como evidencia real."
    }, indent=2))


if __name__ == "__main__":
    main()
