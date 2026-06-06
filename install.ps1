Write-Host "Installing ReconX..."
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -e .
Write-Host "Installation complete. Run 'reconx' to start."
