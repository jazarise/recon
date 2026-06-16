# API Layer Audit

The ReconX API layer defines the web REST endpoints through FastAPI.

## Findings

*   The API is relatively clean and contained primarily within `src/reconx/api/`. 
*   **Duplicate API Root:** During the core duplication sweep, an entire nested shadow API was found at `src/reconx/core/reconx/api`. This has been completely archived to `archive/duplicate/`.
*   **Circular Dependencies:** Analyzed imports across `src/reconx/api`. The main routing structure (`main.py`) correctly aggregates sub-routers (`routes/scans.py`, `routes/auth.py`, `plugin_routes.py`, etc.) without incurring circular logic back from the Core execution logic. 
*   **Structure:** No duplicate routes were identified between the discrete route controllers.

## Resolution

The application relies completely on `reconx.api.main:app` as the singular ASGI interface, mapping unambiguously down to `reconx.core`.
