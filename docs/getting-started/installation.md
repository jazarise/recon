# Installation Guide

ReconX can be installed using Docker (recommended) or manually from the source.

## Requirements
- Docker and Docker Compose (For containerized deployment)
- Python 3.11+ (For manual installation)
- PostgreSQL 15+ (For manual installation)

## Docker Installation (Recommended)
Using Docker is the easiest way to get started. It automatically configures the PostgreSQL database, networking, and security constraints.

1. Clone the repository:
   ```bash
   git clone https://github.com/reconx/reconx.git
   cd reconx
   ```
2. Copy the example configuration file:
   ```bash
   cp .env.example .env
   ```
3. Start the stack in the background:
   ```bash
   docker compose -f deployment/compose/docker-compose.yml up -d
   ```
4. Verify the installation by checking the health endpoint:
   ```bash
   curl http://localhost:8000/health/live
   ```

## Manual Installation
For developers or non-containerized environments:

1. Clone the repository and enter the directory:
   ```bash
   git clone https://github.com/reconx/reconx.git
   cd reconx
   ```
2. Install Python dependencies:
   ```bash
   pip install -e .
   ```
3. Set your environment variables (especially `DATABASE_URL`):
   ```bash
   export DATABASE_URL="postgresql+asyncpg://user:pass@localhost/reconx"
   export RECONX_ENV="production"
   ```
4. Run database migrations:
   ```bash
   alembic upgrade head
   ```
5. Start the API server:
   ```bash
   reconx api --port 8000
   ```
