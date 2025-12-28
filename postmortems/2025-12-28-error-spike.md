# Postmortem: Error Spike (Chaos Injection)

## Summary
Injected 30% error rate to validate SLO burn-rate alerting.

## Impact
- Increased 5xx/502 error ratio, triggered paging alert.

## Detection
- Alert: SLOAvailabilityBurnRateFast fired via Alertmanager webhook.

## Root Cause
- Intentional fault injection via /api/chaos/errors.

## Resolution
- Disabled chaos mode (rate=0).

## Lessons Learned
- Burn-rate alerts and webhook delivery verified.
- Observability stack correlation confirmed (metrics → alert → logs/traces).

## Action Items
- Add dashboard panels: error ratio per path, top failing endpoints.
- Add latency SLO and burn-rate for p95.
