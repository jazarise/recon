# Installation Guide for v1.0.0

ReconX v1.0.0 is officially distributed via Docker and Source.

## Docker (Recommended)
1. Download the `docker-compose.yml` and `.env.example`.
2. Rename `.env.example` to `.env` and set your `JWT_SECRET_KEY` and `POSTGRES_PASSWORD`.
3. Run `docker compose up -d`.

## From Source
1. Download `ReconX-v1.0.0.tar.gz` and extract it.
2. Install dependencies: `pip install -e .`
3. Configure `export DATABASE_URL=...`
4. Run migrations: `alembic upgrade head`
5. Start the server: `reconx api`
