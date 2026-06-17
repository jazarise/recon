# Scalability Review

This document analyzes the current and future scalability limits of the ReconX platform.

## Current Benchmarks & Limits

### Small Deployments (1–10 Projects)
- **Status**: Excellent.
- ReconX runs comfortably on a single VM (2 vCPU, 4GB RAM) orchestrating all plugins and API requests.

### Medium Deployments (100–500 Projects)
- **Status**: Acceptable.
- Database growth remains manageable (<10GB).
- **Bottlenecks**: Workflow concurrency. Running 50 workflows simultaneously will exhaust the local CPU and memory due to parallel `subprocess` executions.

### Large Deployments (1000+ Projects)
- **Status**: Requires Architectural Changes (v2.0).
- **Bottlenecks**:
  - *Asset Graph Size*: With millions of assets, deduplication checks during the `AssetCorrelator` phase will lock tables or cause high query latency.
  - *Compute*: Single-node plugin execution cannot support enterprise scale.

## Scaling Strategy (v2.0)
To support large-scale enterprise deployments, ReconX must implement:
1. **Horizontal Worker Scaling**: Decoupling the API from the Workflow Engine, passing tasks to a Redis/RabbitMQ queue consumed by scalable worker pods.
2. **Database Partitioning**: Partitioning the `assets` and `findings` tables by `project_id`.
3. **Caching Layer**: Introducing Redis to cache asset deduplication lookups.
