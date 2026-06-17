# Plugin Framework

The Plugin Framework enables ReconX to remain agnostic to the specific offensive security tools used under the hood.

## The `ReconXPlugin` Interface

All plugins must inherit from the `ReconXPlugin` base class provided by the SDK. This enforces a standard contract:

1. **`name`**: The unique identifier for the plugin.
2. **`execute(target)`**: The core method where the tool is invoked via `subprocess` (securely).
3. **`parse(output)`**: Converts the tool's raw output into ReconX's standardized `Asset` or `Finding` dictionaries.

## Sandboxing

Plugins are run using a restricted `subprocess.run` context. The framework strictly forbids `shell=True` to prevent shell injection vulnerabilities. Execution is restricted to the specific binaries defined in the plugin's metadata.
