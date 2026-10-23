"""Carga reproducible de la ruta FastAPI con modelo de prueba (NO modelo MLflow real).

Se usa cuando mlflow.db/mlruns no están disponibles en el ZIP. El resultado verifica
el endpoint, validación HTTP y concurrencia básica de la app con un modelo determinista;
NO representa rendimiento del modelo de producción ni sustituye la prueba con el artefacto real.
"""
import concurrent.futures
import importlib
import json
import sys
import tempfile
import time
import types
from pathlib import Path

from fastapi.testclient import TestClient

class DummyModel:
    def predict(self, rows):
        return [int(sum(rows[0]) > 0)]
    def predict_proba(self, rows):
        score = 0.7 if sum(rows[0]) > 0 else 0.3
        return [[1-score, score]]


def main(total=200, workers=25):
    mlflow = types.ModuleType('mlflow')
    mlflow.set_tracking_uri = lambda *_a, **_k: None
    mlflow_sklearn = types.ModuleType('mlflow.sklearn')
    mlflow_sklearn.load_model = lambda *_a, **_k: DummyModel()
    mlflow.sklearn = mlflow_sklearn
    sys.modules['mlflow'] = mlflow
    sys.modules['mlflow.sklearn'] = mlflow_sklearn
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    sys.modules.pop('serving.app', None)
    appmod = importlib.import_module('serving.app')
    with tempfile.TemporaryDirectory() as td:
        appmod.LOG_PATH = Path(td) / 'predictions.csv'
        import monitoring.logger as logger_module
        logger_module.LOG_PATH = appmod.LOG_PATH
        payload = {'features': [0.1] * 20}
        latencies = []
        statuses = []
        start = time.perf_counter()
        def call(_):
            t0 = time.perf_counter()
            with TestClient(appmod.app) as client:
                response = client.post('/predict', json=payload)
            return response.status_code, (time.perf_counter()-t0)*1000
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
            results = list(pool.map(call, range(total)))
        elapsed = time.perf_counter()-start
        statuses = [x[0] for x in results]
        latencies = sorted(x[1] for x in results)
        p95 = latencies[min(len(latencies)-1, int(0.95*len(latencies)))]
        output = {
            'test_type': 'FASTAPI_ROUTE_WITH_DUMMY_MODEL_NOT_PRODUCTION',
            'requests': total,
            'workers': workers,
            'successes_200': sum(s == 200 for s in statuses),
            'errors': sum(s != 200 for s in statuses),
            'elapsed_seconds': round(elapsed, 3),
            'requests_per_second': round(total/elapsed, 2),
            'p95_latency_ms': round(p95, 2),
            'model': 'deterministic dummy model; MLflow artifact not loaded',
            'limitations': 'In-process TestClient, no network/container overhead; not production benchmark.'
        }
        out = Path(__file__).resolve().parents[1] / 'evidencias' / 'auditoria' / 'stress_test_stub.json'
        out.write_text(json.dumps(output, indent=2), encoding='utf-8')
        print(json.dumps(output, indent=2))

if __name__ == '__main__':
    main()
