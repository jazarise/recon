import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text, JSON, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class ScanModel(Base):
    __tablename__ = "scans"

    id = Column(String, primary_key=True, index=True)
    workflow = Column(String, index=True)
    target = Column(String, index=True)
    status = Column(String)
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)

    # Relationships
    workflow_runs = relationship("WorkflowRunModel", back_populates="scan", cascade="all, delete-orphan")
    findings = relationship("FindingModel", back_populates="scan", cascade="all, delete-orphan")
    assets = relationship("AssetModel", back_populates="scan", cascade="all, delete-orphan")


class WorkflowRunModel(Base):
    __tablename__ = "workflow_runs"
    
    id = Column(String, primary_key=True, index=True)
    scan_id = Column(String, ForeignKey("scans.id", ondelete="CASCADE"), index=True, nullable=False)
    status = Column(String)
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)
    
    scan = relationship("ScanModel", back_populates="workflow_runs")
    plugin_results = relationship("PluginResultModel", back_populates="workflow_run", cascade="all, delete-orphan")


class PluginResultModel(Base):
    __tablename__ = "plugin_results"
    
    id = Column(String, primary_key=True, index=True)
    workflow_run_id = Column(String, ForeignKey("workflow_runs.id", ondelete="CASCADE"), index=True, nullable=False)
    plugin_name = Column(String, index=True)
    category = Column(String, index=True)
    success = Column(Boolean, default=True)
    data = Column(JSON, default=dict)
    errors = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    workflow_run = relationship("WorkflowRunModel", back_populates="plugin_results")


class AssetModel(Base):
    __tablename__ = "assets"
    
    id = Column(String, primary_key=True, index=True)
    scan_id = Column(String, ForeignKey("scans.id", ondelete="CASCADE"), index=True, nullable=False)
    type = Column(String, index=True)
    value = Column(String, index=True)
    source = Column(String)
    confidence = Column(Float, default=1.0)
    tags = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    scan = relationship("ScanModel", back_populates="assets")
    findings = relationship("FindingModel", back_populates="asset", cascade="all, delete-orphan")
    
    # Relationships for RelationshipModel
    relationships_as_source = relationship("RelationshipModel", foreign_keys="[RelationshipModel.source_asset_id]", back_populates="source_asset_rel", cascade="all, delete-orphan")
    relationships_as_target = relationship("RelationshipModel", foreign_keys="[RelationshipModel.target_asset_id]", back_populates="target_asset_rel", cascade="all, delete-orphan")


class FindingModel(Base):
    __tablename__ = "findings"
    
    id = Column(String, primary_key=True, index=True)
    scan_id = Column(String, ForeignKey("scans.id", ondelete="CASCADE"), index=True, nullable=False)
    title = Column(String)
    severity = Column(String, index=True)
    asset_id = Column(String, ForeignKey("assets.id", ondelete="CASCADE"), nullable=True, index=True)
    capability = Column(String, index=True)
    source = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    scan = relationship("ScanModel", back_populates="findings")
    asset = relationship("AssetModel", back_populates="findings")


class RelationshipModel(Base):
    __tablename__ = "relationships"
    
    id = Column(String, primary_key=True, index=True)
    source_asset_id = Column(String, ForeignKey("assets.id", ondelete="CASCADE"), index=True, nullable=False)
    target_asset_id = Column(String, ForeignKey("assets.id", ondelete="CASCADE"), index=True, nullable=False)
    type = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    source_asset_rel = relationship("AssetModel", foreign_keys=[source_asset_id], back_populates="relationships_as_source")
    target_asset_rel = relationship("AssetModel", foreign_keys=[target_asset_id], back_populates="relationships_as_target")


class EvidenceModel(Base):
    __tablename__ = "evidence"
    
    id = Column(String, primary_key=True, index=True)
    source = Column(String, index=True)
    raw_data = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
