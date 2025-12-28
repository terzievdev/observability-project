Observability Project – Full LGTM Stack
Overview

This project demonstrates a production-style observability stack built end-to-end using modern CNCF tooling.

The goal is not only to collect metrics, logs, and traces, but to operate a system using SLOs, burn-rate alerting, and incident response workflows, including chaos testing and postmortems.

This repository is designed as a portfolio-grade DevOps / SRE demonstration, focusing on operability rather than simple deployment.

Architecture
Stack Components

Metrics: Prometheus

Logs: Loki + Promtail

Traces: Tempo

Dashboards & Visualization: Grafana

Alerting: Alertmanager

Telemetry: OpenTelemetry Collector

Workload

Python API instrumented with OpenTelemetry

Load generator producing continuous traffic

Chaos endpoints for error and latency injection

Alerting Model

SLO-based burn rate alerts

Fast burn alerts

Slow burn alerts

Webhook delivery to a custom alert receiver

Project Structure
observability-project/
├── app/                 # Instrumented Python API
├── loadgen/             # Traffic generator
├── alert-logger/        # Alertmanager webhook receiver
├── prometheus/          # Prometheus config and alert rules
├── grafana/             # Provisioned datasources
├── dashboards/          # Grafana dashboards
├── loki/
├── tempo/
├── otel-collector/
├── runbooks/            # Incident response runbooks
├── postmortems/         # Incident postmortems
├── docker-compose.yml
└── README.md

How to Run
Prerequisites

Docker Desktop

Docker Compose v2

Start the Stack
docker compose up -d --build

Access Points
Service	URL
API	http://localhost:8080

Grafana	http://localhost:3000
 (admin/admin)
Prometheus	http://localhost:9090

Alertmanager	http://localhost:9093
Observability Capabilities
Metrics

Request rate

Error rate

Latency (p95)

SLO error budget burn rate

Logs

Structured application logs

Centralized via Loki

Correlated with metrics and traces

Traces

Distributed traces collected via OpenTelemetry

Visualized in Grafana Tempo

SLOs and Alerting
Availability SLO

Target: 99.9% availability

Error budget: 0.1%

Alerts

Fast burn rate alerts (5m + 1h windows)

Slow burn rate alerts (30m + 6h windows)

High latency p95 alerts

Alerts are routed via Alertmanager to a webhook receiver (alert-logger).

Chaos Engineering
Inject Error Spike
curl -X POST http://localhost:8080/api/chaos/errors?rate=0.3

Inject Latency
curl -X POST http://localhost:8080/api/chaos/latency?ms=800

Disable Chaos
curl -X POST http://localhost:8080/api/chaos/errors?rate=0
curl -X POST http://localhost:8080/api/chaos/latency?ms=0

Incident Response
Runbooks

Incident response procedures are documented in:

runbooks/

Postmortems

Completed incident analyses are documented in:

postmortems/


Postmortems follow a simplified SRE-style incident lifecycle:

Detection

Impact assessment

Root cause analysis

Mitigation

Lessons learned

Why This Project Exists

This project focuses on operability, not just deployment.

It demonstrates:

Practical observability instead of tool collection

SLO-driven alerting rather than static thresholds

Correlation of metrics, logs, and traces

An incident response mindset (runbooks and postmortems)

Future Improvements

Per-endpoint SLOs

Error budget dashboards

Synthetic monitoring

CI pipeline for validation and linting

Kubernetes deployment variant