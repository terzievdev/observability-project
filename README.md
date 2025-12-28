🔥 CLEAN README
🔭 Observability Project – LGTM Stack with SLOs
📌 Overview

This project demonstrates a production-style observability stack with:

Metrics, logs, and traces correlation

SLO-based burn rate alerting

Chaos engineering and incident simulation

Documented incident response (runbooks + postmortems)

Designed as a DevOps / SRE portfolio project.

🧱 Stack

Observability

Metrics: Prometheus

Logs: Loki + Promtail

Traces: Tempo

Dashboards: Grafana

Alerting: Alertmanager

Telemetry: OpenTelemetry Collector

Workload

Python API instrumented with OpenTelemetry

Load generator producing continuous traffic

Chaos endpoints for error & latency injection

🚦 Alerting Model

SLO-based burn rate alerts

Fast burn alerts (paging)

Slow burn alerts (ticket)

Webhook delivery to custom alert receiver

📁 Project Structure
observability-project/
├── app/              # Instrumented Python API
├── loadgen/          # Traffic generator
├── alert-logger/     # Alertmanager webhook receiver
├── prometheus/       # Prometheus config & rules
├── grafana/          # Provisioned datasources
├── dashboards/       # Grafana dashboards
├── loki/
├── tempo/
├── otel-collector/
├── runbooks/         # Incident response runbooks
├── postmortems/      # Incident postmortems
├── docker-compose.yml
└── README.md

▶️ How to Run
Prerequisites

Docker Desktop

Docker Compose v2

Start the stack
docker compose up -d --build

🌍 Access Points
Service	URL
API	http://localhost:8080

Grafana	http://localhost:3000
 (admin / admin)
Prometheus	http://localhost:9090

Alertmanager	http://localhost:9093
📊 Observability Capabilities

Metrics

Request rate

Error rate

Latency (p95)

Error budget burn rate

Logs

Structured application logs via Loki

Traces

Distributed traces via Tempo

💥 Chaos Engineering
Inject error spike
curl -X POST http://localhost:8080/api/chaos/errors?rate=0.3

Inject latency
curl -X POST http://localhost:8080/api/chaos/latency?ms=800

Disable chaos
curl -X POST http://localhost:8080/api/chaos/errors?rate=0
curl -X POST http://localhost:8080/api/chaos/latency?ms=0

🚑 Incident Response

Runbooks: runbooks/

Postmortems: postmortems/

Alerts trigger an incident flow:
metrics → alert → webhook → investigation → resolution → postmortem

🎯 Why This Project

This project focuses on operability, not just deployment.

It demonstrates:

Real SLO-based alerting (not static thresholds)

Metrics, logs, and traces correlation

Chaos testing and incident validation

Production-style documentation

🚀 Future Improvements

Per-endpoint SLOs

Error budget dashboards

Synthetic monitoring

CI validation pipeline

Kubernetes deployment
