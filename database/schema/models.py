import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AssetModel(Base):
    __tablename__ = "assets"
    
    id = Column(String, primary_key=True, index=True)
    type = Column(String, index=True)
    value = Column(String, index=True)
    source = Column(String)
    confidence = Column(Float, default=1.0)
    tags = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class FindingModel(Base):
    __tablename__ = "findings"
    
    id = Column(String, primary_key=True, index=True)
    title = Column(String)
    severity = Column(String, index=True)
    asset_id = Column(String, ForeignKey("assets.id"), nullable=True)
    capability = Column(String, index=True)
    source = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class RelationshipModel(Base):
    __tablename__ = "relationships"
    
    id = Column(String, primary_key=True, index=True)
    source_asset = Column(String, ForeignKey("assets.id"), index=True)
    target_asset = Column(String, ForeignKey("assets.id"), index=True)
    type = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class EvidenceModel(Base):
    __tablename__ = "evidence"
    
    id = Column(String, primary_key=True, index=True)
    source = Column(String, index=True)
    raw_data = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ScanModel(Base):
    __tablename__ = "scans"

    id = Column(String, primary_key=True, index=True)
    workflow = Column(String, index=True)
    target = Column(String, index=True)
    status = Column(String)
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)
