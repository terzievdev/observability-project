FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir \
  fastapi==0.115.6 uvicorn[standard]==0.32.1 \
  prometheus-client==0.21.1 \
  opentelemetry-api==1.29.0 \
  opentelemetry-sdk==1.29.0 \
  opentelemetry-exporter-otlp==1.29.0 \
  opentelemetry-instrumentation==0.50b0 \
  opentelemetry-instrumentation-fastapi==0.50b0 \
  opentelemetry-instrumentation-logging==0.50b0 \
  opentelemetry-instrumentation-requests==0.50b0

COPY . .
CMD ["python", "main.py"]
