# Alerting Framework

## Alert Matrices
### Critical (PagerDuty Webhook)
- 5xx Error Rate > 5% over 5m
- Database connectivity lost
- Workflow Engine Queue Backlog > 10,000

### High (Slack Channel)
- Worker node crashed (OOM)
- CPU utilization > 85% across pool

### Medium (Daily Summary)
- API P99 Latency > 1s
