# Plugin Development Guide

To develop a new plugin:
1. Inherit from `sdk.plugin_base.BasePlugin`.
2. Implement the `execute()` async method.
3. Yield/Return instances of `core.models.finding.Finding`.
4. Register the plugin in `registry/plugin_registry.yaml`.
