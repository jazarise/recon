# Circular Dependencies Report

### Circular Dependency: core <-> modules
- **Module A:** core
- **Module B:** modules
- **Impact:** Circular import blocks clean initialization and testing.
- **Resolution:** Decouple dependency, potentially by moving shared interfaces to core.

