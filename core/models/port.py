from dataclasses import dataclass

@dataclass
class Port:
    host: str
    port: int
    protocol: str = "tcp"
