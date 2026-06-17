# Contributing to ReconX

First off, thank you for considering contributing to ReconX! It's people like you that make ReconX such a great platform.

## Getting Started
1. Fork the repository on GitHub.
2. Clone the fork locally.
3. Install dependencies: `pip install -e .[dev]`
4. Create a branch: `git checkout -b feature/your-feature-name`

## Coding Standards
- We strictly follow PEP 8.
- Code is formatted using `ruff`. Run `ruff format .` before committing.
- Static typing is enforced. Run `mypy src` and ensure no new errors are introduced.
- Security linting is checked via `bandit -r src`.

## Branch Naming
- Features: `feature/<short-desc>`
- Bugfixes: `fix/<short-desc>`
- Docs: `docs/<short-desc>`

## Commit Format
Use Conventional Commits:
`feat: added new asset normalizer`
`fix: resolved issue with subfinder plugin failing`
`docs: updated workflow examples`

## Testing Requirements
- No bug fix without a test.
- Features must include unit tests.
- Run `pytest` locally to ensure the suite passes.

## Review Process
1. Push your branch and open a Pull Request against `main`.
2. Ensure CI pipelines pass.
3. Wait for code review from a core maintainer.
