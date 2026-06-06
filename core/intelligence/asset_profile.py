from core.database.session import SessionLocal
from core.database.models import DBFinding
from core.risk.engine import risk_engine

class AssetProfile:
    def __init__(self, asset_value: str):
        self.asset = asset_value
        self.ips = set()
        self.ports = set()
        self.technologies = set()
        self.vulnerabilities = []
        self.risk_score = 0
        
    def build(self):
        db = SessionLocal()
        findings = db.query(DBFinding).filter(DBFinding.source == self.asset).all()
        
        for f in findings:
            if f.category == "ip":
                self.ips.add(f.value)
            elif f.category == "port":
                self.ports.add(f.value)
            elif f.category == "technology":
                self.technologies.add(f.value)
            elif f.category == "vulnerability":
                self.vulnerabilities.append(f)
                
        self.risk_score = risk_engine.calculate_asset_risk(self.vulnerabilities)
        db.close()
        return self
