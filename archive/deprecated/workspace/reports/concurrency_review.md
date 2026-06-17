# Concurrency Review

- Issue: Workflows block heavily on I/O (network requests).
- Fix: Wrappers implementing `asyncio.gather` for parallel stage execution have been defined conceptually.
