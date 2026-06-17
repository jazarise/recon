# Your First Scan

While the Quick Start covered the command line, this page provides a deeper look into what actually happens during your first scan.

## Workflow Execution
When you run `reconx workflow run passive_recon example.com`:

1. **Orchestration**: The `WorkflowEngine` loads the `passive_recon.yaml` specification.
2. **Task Queueing**: Tasks like Subfinder and Assetfinder are queued in parallel, as they don't depend on each other.
3. **Execution**: The `PluginManager` executes the plugins securely inside isolated contexts.
4. **Data Normalization**: Raw tool output (JSON, text) is passed to the `AssetNormalizer`. 
5. **Correlation**: The `AssetCorrelator` maps the new assets to existing ones, building relationships (e.g., `api.example.com` is a subdomain of `example.com`).

## Analyzing the Output
ReconX doesn't just store flat lists. It builds an **Intelligence Graph**. You can query this graph via the API to answer questions like:

- *"What IPs resolve to this subdomain?"*
- *"Are there any High severity findings on assets running Nginx?"*

To view the execution trace of your scan:
```bash
reconx workflow status <EXECUTION_ID>
```
