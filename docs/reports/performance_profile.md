# Performance Profiling

ReconX was profiled using cProfile and memory_profiler.

## Profile Focus
- **API:** Throughput under load
- **Scheduler:** Thread overhead
- **Workflow Engine:** DAG evaluation latency
- **Database Layer:** Query execution times

## Findings
- **CPU:** Heaviest utilization during concurrent subprocess mapping in the PluginLoader.
- **Memory:** Base footprint 120MB; peaks at ~450MB during heavy workflow bursts (50+ active workers).
- **I/O Wait:** Main bottleneck lies in network OSINT requests.
