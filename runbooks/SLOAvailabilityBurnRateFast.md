# Runbook: SLOAvailabilityBurnRateFast

## Meaning
Fast error budget burn. Investigate immediately.

## Triage
1. Check error ratio:
   - Prometheus: slo:availability:error_ratio_5m and _1h
2. Check API errors:
   - Prometheus: sum(rate(http_requests_total{status=~"5..|502"}[1m]))
3. Check recent deploys / config changes (N/A in demo, but document it)
4. Drill down:
   - Grafana Explore (Prometheus) → identify endpoint spikes by `path`
   - Grafana Explore (Loki) → {service="api"} around incident time
   - Grafana Explore (Tempo) → trace search for `service.name=api`

## Mitigation
- If caused by chaos: disable:
  - POST /api/chaos/errors?rate=0
- If real dependency issue: reduce traffic, rollback, or degrade features (document what you’d do)

## Verification
- Alerts resolve
- Error ratio back below SLO burn thresholds
