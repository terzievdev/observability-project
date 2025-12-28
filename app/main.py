import os
import time
import random
import logging
from typing import Optional

from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor

SERVICE_NAME = os.getenv("SERVICE_NAME", "api")
OTEL_EXPORTER_OTLP_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4318")

# ---- Logging with trace context ----
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
LoggingInstrumentor().instrument(set_logging_format=True)
logger = logging.getLogger(SERVICE_NAME)

# ---- Tracing ----
resource = Resource.create({"service.name": SERVICE_NAME})
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=f"{OTEL_EXPORTER_OTLP_ENDPOINT}/v1/traces"))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

# ---- Metrics ----
REQUESTS = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["service", "method", "path", "status"]
)

LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["service", "method", "path"],
    buckets=(0.01, 0.025, 0.05, 0.1, 0.2, 0.3, 0.5, 0.75, 1.0, 2.0, 5.0)
)

# ---- Chaos config in-memory ----
CHAOS_LATENCY_MS = 0
CHAOS_ERROR_RATE = 0.0  # 0..1

app = FastAPI(title="Observability Demo API")

FastAPIInstrumentor.instrument_app(app)

def maybe_chaos_latency():
    global CHAOS_LATENCY_MS
    if CHAOS_LATENCY_MS > 0:
        time.sleep(CHAOS_LATENCY_MS / 1000.0)

def maybe_chaos_error():
    global CHAOS_ERROR_RATE
    if CHAOS_ERROR_RATE > 0 and random.random() < CHAOS_ERROR_RATE:
        return True
    return False

@app.middleware("http")
async def metrics_middleware(request, call_next):
    start = time.time()
    path = request.url.path
    method = request.method

    maybe_chaos_latency()

    try:
        response = await call_next(request)
        status = str(response.status_code)
        return response
    except Exception as e:
        status = "500"
        logger.exception("Unhandled error: %s", e)
        return JSONResponse({"error": "internal"}, status_code=500)
    finally:
        dur = time.time() - start
        REQUESTS.labels(SERVICE_NAME, method, path, status).inc()
        LATENCY.labels(SERVICE_NAME, method, path).observe(dur)

@app.get("/api/hello")
def hello():
    with tracer.start_as_current_span("hello-handler"):
        if maybe_chaos_error():
            logger.error("Chaos error triggered on /api/hello")
            return JSONResponse({"error": "chaos"}, status_code=500)

        logger.info("Hello called")
        return {"service": SERVICE_NAME, "message": "hello"}

@app.get("/api/db")
def db_sim():
    with tracer.start_as_current_span("db-sim"):
        # simulate downstream call latency
        t = random.uniform(0.02, 0.25)
        time.sleep(t)

        if maybe_chaos_error():
            logger.error("Chaos error triggered on /api/db")
            return JSONResponse({"error": "db-downstream"}, status_code=502)

        logger.info("db_sim ok (sleep=%.3f)", t)
        return {"ok": True, "sleep": t}

@app.post("/api/chaos/latency")
def set_latency(ms: int):
    global CHAOS_LATENCY_MS
    CHAOS_LATENCY_MS = max(0, ms)
    logger.warning("CHAOS latency set to %d ms", CHAOS_LATENCY_MS)
    return {"latency_ms": CHAOS_LATENCY_MS}

@app.post("/api/chaos/errors")
def set_errors(rate: float):
    global CHAOS_ERROR_RATE
    CHAOS_ERROR_RATE = min(max(rate, 0.0), 1.0)
    logger.warning("CHAOS error rate set to %.3f", CHAOS_ERROR_RATE)
    return {"error_rate": CHAOS_ERROR_RATE}

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
