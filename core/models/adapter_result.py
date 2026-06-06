from typing import List
from pydantic import BaseModel
from .asset import Asset
from .finding import Finding
from .relationship import Relationship
from .evidence import Evidence

class AdapterResult(BaseModel):
    assets: List[Asset] = []
    findings: List[Finding] = []
    relationships: List[Relationship] = []
    evidence: List[Evidence] = []
