# Workflow Authoring

Create YAML definitions in `src/reconx/workflows/`.

```yaml
name: basic_scan
stages:
  - id: nmap
    plugin: nmap_wrapper
    depends_on: []
```
