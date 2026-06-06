# ReconX Workflow Guide

## Custom Workflows
ReconX uses YAML to define execution graphs.

### Example: `custom.yaml`
```yaml
name: Custom Web Assessment
steps:
  - id: s1
    plugin: dns_intelligence
    timeout: 60
  - id: s2
    plugin: web_recon
    timeout: 300
```

### Execution
Run your custom workflow via the CLI:
`python reconx.py workflow custom.yaml --target example.com`

The workflow engine will automatically resolve dependencies and execute plugins in parallel where possible.
