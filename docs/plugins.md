# Plugins

Plugins execute atomic tasks (e.g. Subfinder, Nmap).
They are dynamically loaded by the `Orchestrator` based on workflow dependencies.
Each plugin must return `Finding` objects.
