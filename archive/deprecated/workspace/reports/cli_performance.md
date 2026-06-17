# CLI Performance

- Analysis: Loading the help menu evaluates the entire plugin tree.
- Optimization: Decouple help-text generation from plugin initialization, parsing static text metadata directly.
