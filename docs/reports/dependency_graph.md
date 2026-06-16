# Dependency Graph

This maps relationships between core modules:

`mermaid
graph TD
    api --> core
    api --> database
    cli --> core
    core --> modules
    core --> database
    modules --> core
    plugins --> core
`
