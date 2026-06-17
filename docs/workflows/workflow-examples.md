# Workflow Examples

Here are some example workflows demonstrating parallel and sequential execution.

## Single Plugin
```yaml
name: simple_scan
description: Runs only subfinder
tasks:
  - id: t1
    plugin: 
      name: subfinder
```

## Parallel Execution
Because neither task defines `depends_on`, they will run simultaneously.
```yaml
name: passive_recon
description: Passive subdomain enumeration
tasks:
  - id: subfinder_task
    plugin: 
      name: subfinder
  - id: assetfinder_task
    plugin:
      name: assetfinder
```

## Sequential Pipeline
This pipeline finds subdomains, then actively probes them for open ports.
```yaml
name: full_recon
description: End-to-end recon
tasks:
  - id: enumerate_subdomains
    plugin:
      name: subfinder
  - id: scan_ports
    plugin:
      name: naabu
    depends_on:
      - enumerate_subdomains
```
