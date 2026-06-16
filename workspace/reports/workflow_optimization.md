# Workflow Optimization

- Analysis: Workflows pass state inefficiently via synchronous dict copies.
- Improvement: Establish asynchronous generators (`yield` streams) to pass state between stages without memory bloat.
