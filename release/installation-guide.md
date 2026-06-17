# Installation Guide for Release v1.0.0

1. **Unpack the release:**
   ```bash
   tar -xzvf reconx-v1.0.0.tar.gz
   cd reconx-v1.0.0
   ```

2. **Run via Docker:**
   ```bash
   docker compose -f deployment/compose/docker-compose.yml up -d
   ```

3. **Verify:**
   ```bash
   curl http://localhost:8000/health/live
   ```
