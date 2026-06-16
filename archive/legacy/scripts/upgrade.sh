#!/bin/bash
echo "Upgrading ReconX..."
git pull origin main
source .venv/bin/activate
pip install -e .
alembic upgrade head
echo "Upgrade complete."
