# Marketplace Design

## Publishing Lifecycle
1. **Submission:** Developer signs package with PGP.
2. **Validation:** CI runner checks for malicious `os.system` calls.
3. **Review:** Maintainer approval.
4. **Publishing:** Merged to `registry.reconx.local`.
5. **Versioning:** Strict SemVer locking.
