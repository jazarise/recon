# Stage 12: Enterprise Architecture Overview

## Modular Plugin Framework
ReconX now strictly executes isolated modules inside `src/reconx/plugins/`. The `loader.py` layer guarantees drop-in extendability without modifying the core.

## Event-Driven Asynchronous Engine
The `EventBus` pub/sub queue entirely decoupled the DAG linear engine. Plugins now react to specific intelligence vectors (e.g., `NEW_IP_FOUND`) concurrently, speeding up operations.

## Safety Guardrails
`guardrails.py` ensures execution completely halts if an unauthorized target domain is fed to the engine, strictly adhering to authorized/ethical testing paradigms.
