from pydantic import BaseModel
from typing import List, Dict, Any

class ReconResult(BaseModel):
    target: str
    subdomains: List[str] = []
    ips: List[str] = []
    ports: List[int] = []
    tech_stack: List[str] = []
    vulnerabilities: List[str] = []
    metadata: Dict[str, Any] = {}
