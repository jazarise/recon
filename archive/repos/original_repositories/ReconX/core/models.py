from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Asset(Base):
    __tablename__ = 'assets'
    
    id = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False) # 'domain', 'subdomain', 'ip', 'asn', 'url'
    value = Column(String(255), nullable=False, unique=True)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)
    tags = Column(JSON, default=list)

    # Relationships
    services = relationship("Service", back_populates="asset")
    vulnerabilities = relationship("Vulnerability", back_populates="asset")

class Service(Base):
    __tablename__ = 'services'
    
    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey('assets.id'))
    port = Column(Integer, nullable=False)
    protocol = Column(String(20), nullable=False)
    service_name = Column(String(100))
    product = Column(String(100))
    version = Column(String(100))
    last_seen = Column(DateTime, default=datetime.utcnow)
    
    asset = relationship("Asset", back_populates="services")

class Vulnerability(Base):
    __tablename__ = 'vulnerabilities'
    
    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey('assets.id'))
    name = Column(String(255), nullable=False)
    severity = Column(String(50))
    description = Column(Text)
    discovered_at = Column(DateTime, default=datetime.utcnow)
    
    asset = relationship("Asset", back_populates="vulnerabilities")

class ScanHistory(Base):
    __tablename__ = 'scan_history'
    
    id = Column(Integer, primary_key=True)
    workflow_id = Column(String(100), nullable=False, unique=True)
    target = Column(String(255), nullable=False)
    mode = Column(String(50))
    status = Column(String(50))
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    raw_results = Column(JSON)
