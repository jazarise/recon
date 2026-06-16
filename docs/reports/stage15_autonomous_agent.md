# Stage 15: Autonomous Agent Architecture

## Multi-Agent Triad
The ReconX framework now utilizes an Orchestrator bridging three conceptual agents:
- **PlannerAgent:** Dynamically generates the sequence of reconnaissance actions based on the user-defined string `--goal`.
- **ExecutionAgent:** Operates the modules asynchronously.
- **AnalysisAgent:** Evaluates the efficacy of the payloads returning to the State Memory.

## Auto-Stop Guardrails
The system implements a hard stop counter. If the AnalysisAgent records 3 consecutive cycles yielding 0 new intelligence (diminishing returns), the Orchestrator terminates all execution instantly, preventing infinite autonomous loops.
