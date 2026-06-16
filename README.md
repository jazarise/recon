# ReconX v3.0

ReconX is an autonomous, declarative Offensive Security Reconnaissance Framework.

## Features
- **Declarative YAML Workflows:** Chain plugins as a Directed Acyclic Graph.
- **Async Execution:** Heavy parallelization using asyncio and thread pools.
- **Plugin Architecture:** Write tools in bash or python and wrap them natively.
- **REST API:** Control execution dynamically via FastAPI.

## Quick Start
```bash
git clone https://github.com/reconx/reconx.git
pip install -e .
reconx init
reconx run workflow deep_scan
```
