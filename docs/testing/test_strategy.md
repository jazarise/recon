# Test Strategy Document

This document outlines the testing pyramid and baseline targets required for ReconX.

## Test Pyramid

ReconX enforces a strict Testing Pyramid distribution to ensure fast local feedback loops and robust integration gates.

| Test Type | Target Distribution | Purpose | Framework |
| --------- | ------------------- | ------- | --------- |
| **Unit** | 70% | Validating isolated classes, parsers, and atomic business logic. | `pytest` |
| **Integration** | 20% | Validating connections between modules (e.g., API -> DB, Plugin -> Scheduler). | `pytest` + `unittest.mock` |
| **E2E / System** | 10% | Validating complete reconnaissance lifecycles (Start to Report). | `pytest` + `FastAPI.TestClient` |

## Infrastructure & Conventions
- **Test Directory:** All tests reside strictly in `tests/`.
- **Framework:** `pytest` is the authoritative runner.
- **Fixtures:** Reusable stubs are centrally located in `tests/conftest.py`.
- **Coverage:** Enforcement targets 80%+ via `pytest-cov`.

## Execution
- Local developers must run `pytest` before commits.
- CI/CD automatically enforces coverage and static analysis gates on all PRs.
