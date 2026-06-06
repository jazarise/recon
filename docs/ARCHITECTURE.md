# ReconX Architecture Overview

This document provides a high-level overview of the ReconX architecture post Stage 0 cleanup.

## Core Components
- **CLI**: Entry point for command-line execution.
- **Core**: Contains `ai`, `database`, `analytics`, etc.
- **Modules**: Native modules like `discovery`, `web`, `dns`.
- **Plugins**: Categorized external capabilities (e.g. `vuln`, `reporting`).
- **Workflows**: Defined automation scripts orchestrating the platform.
