from dataclasses import dataclass

@dataclass
class Target:
    value: str
    type: str  # domain, subdomain, ip, cidr, url, organization, email
