# Benchmark Results (v1.0.0)

Hardware: 2 vCPU, 4GB RAM (Standard Worker Node)

## Plugin Execution
| Plugin | Target Size | Average Runtime | Peak Memory |
| ------ | ----------- | --------------- | ----------- |
| Subfinder | 1 Domain | 4.2s | 45MB |
| Httpx | 100 Subdomains | 12.1s | 60MB |
| Katana | 1 Domain | 25.4s | 85MB |
| Nuclei | 100 URLs | 45.8s | 110MB |

## Workflow Runtime
| Workflow | Configuration | Average Total Runtime |
| -------- | ------------- | --------------------- |
| Passive Recon | Subfinder + Assetfinder (Parallel) | 5.1s |
| Web Recon | Subfinder -> Httpx | 16.5s |
| Full Recon | Subfinder -> Httpx -> Nuclei | 62.3s |

## Reporting
| Format | Dataset Size | Generation Time |
| ------ | ------------ | --------------- |
| JSON | 10,000 Assets | 0.8s |
| CSV | 10,000 Assets | 1.1s |
| PDF | 500 Findings | 3.4s |

**Conclusion**: Single-node performance is well within acceptable margins for small to medium assessments.
