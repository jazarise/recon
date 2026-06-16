# ADR-001: Plugin System Single Loader Architecture

## Context
ReconX utilizes a wide array of dynamic plugins representing different OSINT sources and Scanners. During the Stage 2 architecture audit, it was discovered that there were multiple plugin loading abstractions across the project, including a standalone registry embedded inside the `core` layer and hundreds of nested `package.json` registries belonging to individual node scripts in experimental repositories. This fragmented the plugin lifecycle and made unified validation impossible.

## Decision
ReconX standardizes on a **Single Plugin Lifecycle** natively driven by Python.
- All plugins must inherit from `reconx.core.reconx.plugins.base.Plugin` (or the `ReconXPlugin` adapter).
- The `reconx.core.plugin_manager.loader.PluginManager` is the singular, authoritative mechanism for loading, validating, and instantiating plugins. 
- Standalone JSON registries (e.g., `plugin_registry.json`) are forbidden.

## Consequences
- **Positive:** Centralized validation logic ensures all plugins adhere to the correct lifecycle (`load`, `validate`, `execute`, `cleanup`).
- **Negative:** Node-based experimental scripts must be wrapped tightly within a Python `ToolAdapter`, adding a minor abstraction layer.

## Alternatives Considered
- Maintaining an external `JSON` or `YAML` registry to index plugins without instantiating Python objects. Rejected because it led to de-syncing between the source tree and the manifest.
