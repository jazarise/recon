# Canonical Native Module Map

| Capability String | Canonical Implementation File |
|---|---|
| `discovery.subdomains` | `modules/discovery/subdomains.py` |
| `dns.resolve` | `modules/dns/resolver.py` |
| `web.probe` | `modules/web/probe.py` |
| `osint.email` | `modules/osint/email.py` |

**Design Rule**: A capability string MUST map to exactly one native implementation or be entirely deferred to the Plugin Engine. There can be no parallel native execution layers.
