# API Extension Guide

To add new REST endpoints, mount a new APIRouter in `core/reconx/api/` and attach it to the root FastAPI app in `core/reconx/cli/main.py` using `app.include_router()`.
