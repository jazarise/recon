# Release Lifecycle

ReconX follows a rigorous release pipeline:

### Experimental
- **Branch:** `develop` or Feature Branches
- **Audience:** Core Developers
- **Stability:** Low. Features are untested and APIs may break daily.

### Beta (Release Candidate)
- **Branch:** `release/*`
- **Audience:** Early Adopters & Reviewers
- **Stability:** High. Feature freeze is enacted. Only bug fixes permitted.

### Stable
- **Branch:** `main` (Tagged e.g., `v2.1.0`)
- **Audience:** Production Operators
- **Stability:** Guaranteed. Has passed full CI/CD, Pytest suites, and Security Audits.

Releases follow Semantic Versioning (`MAJOR.MINOR.PATCH`).
