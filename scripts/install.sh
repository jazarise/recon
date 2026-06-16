#!/bin/bash
echo "Installing ReconX..."
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
echo "Installation complete. Run 'reconx' to start."
