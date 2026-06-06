# Dependency Graphs

ReconX uses `graphlib.TopologicalSorter` to parse workflow dependencies and prevent cycles.

- Independent tools run instantly in parallel.
- Dependent tools wait until all pre-requisite steps (`depends_on`) signal `PluginFinished`.
- If a cycle is detected during `validate_workflow()`, a `DependencyError` is raised immediately.
