# Workflow Development Guide

Workflows are DAGs (Directed Acyclic Graphs).
Define execution nodes via `.yaml` inside `workflows/`. Set `depends_on` array for topological constraints.
