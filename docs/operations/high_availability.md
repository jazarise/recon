# High Availability Planning

## Core HA Model
- **API Nodes:** Run behind an external Load Balancer (Nginx/HAProxy) targeting scaled instances.
- **Worker Pools:** Autoscaling groups keyed on Redis queue depth metric.
- **Database:** Primary/Replica PostgreSQL failover architecture.

## Target Parameters
| Metric | Target   |
| ------ | -------- |
| RPO    | < 15 min |
| RTO    | < 1 hour |
