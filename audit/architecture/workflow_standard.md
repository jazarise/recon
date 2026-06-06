# Unified Workflow System Standard

## Consolidation
Previous iterations of ReconX relied on a mix of python scripts, shell scripts, and custom pipeline formats to run tools.

## The New Standard
We have standardized exclusively on **YAML Workflows** managed by `core.workflow_engine.WorkflowEngine`.

### Structure
Workflows live in the `workflows/` directory.

### Example Schema
```yaml
name: enterprise_recon
description: "Full spectrum discovery and vulnerability mapping"

steps:
  - id: step1_discovery
    plugin: subfinder
    config:
      timeout: 300
      
  - id: step2_resolution
    plugin: dnsx
    depends_on: [step1_discovery]
    
  - id: step3_scanning
    plugin: nuclei
    depends_on: [step2_resolution]
```

### Execution Flow
1. **Target** is provided via CLI (`reconx.py`).
2. **Workflow Engine** parses the YAML.
3. **Execution Manager** invokes the corresponding standardized **Plugins**.
4. Plugins return data that goes strictly to the unified **Findings**.
