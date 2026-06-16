Write-Host "Upgrading ReconX..."
git pull origin main
.\.venv\Scripts\Activate.ps1
pip install -e .
alembic upgrade head
Write-Host "Upgrade complete."
