# Plugin System Optimization

- Pre-optimization Discovery Time: 3500ms
- Proposed AST-Indexing Discovery Time: < 50ms
- Implementation Strategy: Use an LRU-cached index mapping plugin metadata to paths, loading only when executed.
