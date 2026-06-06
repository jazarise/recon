# CLI Design

The CLI uses **Typer** and **Rich**.
- **Typer:** Provides type-hinted, robust command groups (`scan`, `workflow`, `report`, `project`).
- **Rich:** Provides beautiful console output formatting.
- `reconx.py` in the root acts as the central launcher.
