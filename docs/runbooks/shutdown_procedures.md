# Shutdown Procedures

1. Drain workflows via SIGTERM
2. Wait 30s max for graceful exit
3. SIGKILL remaining processes.