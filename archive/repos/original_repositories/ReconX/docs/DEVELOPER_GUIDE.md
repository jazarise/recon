# ReconX Developer Guide

## Setup
1. Clone repo.
2. `python -m venv venv`
3. `pip install -r requirements.txt`

## Testing
Run the test suite using `pytest`.
`python -m pytest tests/`

## Contributing
Ensure any new modules inherit from `PluginInterface` and do not block the asyncio event loop.
Use `ExecutionManager` for subprocess spawning.
