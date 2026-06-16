# Stage 14: AI Engine Architecture

## Heuristics Filtering
We implemented `src/reconx/ai/heuristics.py` to natively classify discovered vectors. Subdomains with keywords like `admin` or `api` are auto-elevated to HIGH, while `cdn` or `static` nodes are demoted to LOW noise.

## Attack Path Graph
The `AttackGraph` module locally tracks nodes mapping DNS relationships (e.g., `example.com -> admin.example.com`), allowing us to visualize structural pivots.

## Next-Best Action Prioritization
Instead of blindly dumping `Port 22` open logs, the `PrioritizationEngine` generates actionable plain-text output in the `ai_exporter.py` recommending specific actions like *"Test authentication bypass on admin.example.com"*.
