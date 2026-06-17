# Intelligence Layer

The Intelligence Layer is the brain of ReconX. It solves the "Data Scattering" problem.

## Normalization
When `subfinder` returns a domain, and `nmap` returns an IP with an open port, the `AssetNormalizer` translates these disparate formats into a unified `Asset` model.

## Deduplication & Correlation
The `AssetCorrelator` analyzes incoming normalized assets against the existing database.
- **Deduplication**: If `example.com` is discovered twice by two different plugins, it is merged into a single database record, tracking multiple sources.
- **Correlation**: If an IP resolves to a Domain, an edge is created in the Graph mapping `Asset(IP) -> Asset(Domain)`.
