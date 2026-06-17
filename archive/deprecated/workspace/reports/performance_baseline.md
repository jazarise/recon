# Performance Baseline

- API Startup: < 150ms
- CLI Startup: < 100ms
- Plugin Loading (Full): 3500ms (Bottleneck)
- CPU: Minimal at idle.
- Recommended Action: Implement AST-based lazy loading for plugins to reduce startup overhead.
