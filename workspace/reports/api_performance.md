# API Performance

- Analysis: Dependency injection is currently evaluating sequentially per request.
- Optimization: Convert DI scopes to singletons where applicable. Enable JSON response serialization via `orjson` instead of standard `json`.
