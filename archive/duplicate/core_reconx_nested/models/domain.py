from typing import List, Optional
from sqlalchemy import String, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from reconx.core.reconx.models.base import Base, TimestampMixin
import enum

class Severity(str, enum.Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Workspace(Base, TimestampMixin):
    __tablename__ = "workspaces"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[Optional[str]] = mapped_column(String)
    
    targets: Mapped[List["Target"]] = relationship(back_populates="workspace")
    scans: Mapped[List["Scan"]] = relationship(back_populates="workspace")

class Target(Base, TimestampMixin):
    __tablename__ = "targets"
    id: Mapped[int] = mapped_column(primary_key=True)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"))
    value: Mapped[str] = mapped_column(String(255)) # IP, domain, etc.
    type: Mapped[str] = mapped_column(String(50))
    
    workspace: Mapped["Workspace"] = relationship(back_populates="targets")
    findings: Mapped[List["Finding"]] = relationship(back_populates="target")

class Scan(Base, TimestampMixin):
    __tablename__ = "scans"
    id: Mapped[int] = mapped_column(primary_key=True)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"))
    status: Mapped[str] = mapped_column(String(50), default="pending")
    plugin_name: Mapped[str] = mapped_column(String(100))
    
    workspace: Mapped["Workspace"] = relationship(back_populates="scans")
    findings: Mapped[List["Finding"]] = relationship(back_populates="scan")

class Finding(Base, TimestampMixin):
    __tablename__ = "findings"
    id: Mapped[int] = mapped_column(primary_key=True)
    target_id: Mapped[Optional[int]] = mapped_column(ForeignKey("targets.id"))
    scan_id: Mapped[Optional[int]] = mapped_column(ForeignKey("scans.id"))
    
    title: Mapped[str] = mapped_column(String(255))
    severity: Mapped[Severity]
    finding_type: Mapped[str] = mapped_column(String(100))
    data: Mapped[dict] = mapped_column(JSON)
    
    target: Mapped[Optional["Target"]] = relationship(back_populates="findings")
    scan: Mapped[Optional["Scan"]] = relationship(back_populates="findings")
    evidence: Mapped[List["Evidence"]] = relationship(back_populates="finding")

class Evidence(Base, TimestampMixin):
    __tablename__ = "evidence"
    id: Mapped[int] = mapped_column(primary_key=True)
    finding_id: Mapped[int] = mapped_column(ForeignKey("findings.id"))
    description: Mapped[str] = mapped_column(String)
    raw_data: Mapped[str] = mapped_column(String)
    
    finding: Mapped["Finding"] = relationship(back_populates="evidence")

class Report(Base, TimestampMixin):
    __tablename__ = "reports"
    id: Mapped[int] = mapped_column(primary_key=True)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"))
    format: Mapped[str] = mapped_column(String(50))
    content: Mapped[Optional[str]] = mapped_column(String)
