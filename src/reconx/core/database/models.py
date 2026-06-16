from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone

Base = declarative_base()

class DBTarget(Base):
    __tablename__ = 'targets'
    id = Column(Integer, primary_key=True)
    value = Column(String(255), nullable=False, unique=True)
    type = Column(String(50), nullable=False)
    
class DBHost(Base):
    __tablename__ = 'hosts'
    id = Column(Integer, primary_key=True)
    ip = Column(String(50), nullable=False, unique=True)
    hostname = Column(String(255))
    
class DBSubdomain(Base):
    __tablename__ = 'subdomains'
    id = Column(Integer, primary_key=True)
    value = Column(String(255), nullable=False, unique=True)
    source = Column(String(100))
    confidence = Column(String(50), default="high")
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class DBPort(Base):
    __tablename__ = 'ports'
    id = Column(Integer, primary_key=True)
    host = Column(String(255), nullable=False)
    port = Column(Integer, nullable=False)
    protocol = Column(String(20), default="tcp")

class DBService(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    host = Column(String(255), nullable=False)
    port = Column(Integer, nullable=False)
    service = Column(String(100), nullable=False)
    version = Column(String(100))
    banner = Column(Text)
    protocol = Column(String(20), default="tcp")

class DBTechnology(Base):
    __tablename__ = 'technologies'
    id = Column(Integer, primary_key=True)
    host = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    version = Column(String(100))

class DBVulnerability(Base):
    __tablename__ = 'vulnerabilities'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    severity = Column(String(50))
    plugin = Column(String(100))
    description = Column(Text)
    evidence = Column(Text)
    recommendation = Column(Text)
    references = Column(JSON)

class DBFinding(Base):
    __tablename__ = 'findings'
    id = Column(Integer, primary_key=True)
    category = Column(String(100), nullable=False)
    value = Column(Text, nullable=False)
    source = Column(String(100))
    metadata_json = Column(JSON)
    scan_id = Column(Integer, ForeignKey('scans.id'), nullable=True)

class DBScan(Base):
    __tablename__ = 'scans'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=True)
    target = Column(String(255), nullable=False)
    workflow = Column(String(100))
    status = Column(String(50), default="running")
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    duration = Column(Float)
    plugins_used = Column(JSON, default=list)
    findings = relationship("DBFinding", backref="scan")

class DBUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="Operator")

class DBProject(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    scans = relationship("DBScan", backref="project")

class DBRelationship(Base):
    __tablename__ = 'relationships'
    id = Column(Integer, primary_key=True)
    source = Column(String(255), nullable=False)
    relation = Column(String(100), nullable=False)
    target = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class DBAssetHistory(Base):
    __tablename__ = 'asset_history'
    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, nullable=False)
    snapshot_json = Column(JSON, nullable=False)
    recorded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class DBFindingHistory(Base):
    __tablename__ = 'finding_history'
    id = Column(Integer, primary_key=True)
    finding_id = Column(Integer, nullable=False)
    status_change = Column(String(50)) # e.g. "new", "resolved"
    recorded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class DBScanHistory(Base):
    __tablename__ = 'scan_history'
    id = Column(Integer, primary_key=True)
    scan_id = Column(Integer, ForeignKey('scans.id'), nullable=False)
    metrics_json = Column(JSON, nullable=False)
    recorded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
