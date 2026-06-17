from sqlalchemy import String, Boolean, ForeignKey, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from reconx.core.database.base import BaseModel
import enum
from typing import List, Optional
from datetime import datetime, timezone


class SeverityEnum(str, enum.Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"
    info = "info"


class User(BaseModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(50), default="viewer")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    projects: Mapped[List["Project"]] = relationship(back_populates="owner")
    refresh_tokens: Mapped[List["RefreshToken"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    sessions: Mapped[List["Session"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    audit_logs: Mapped[List["AuditLog"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    password_history: Mapped[List["PasswordHistory"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Project(BaseModel):
    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    owner_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)

    owner: Mapped["User"] = relationship(back_populates="projects")
    targets: Mapped[List["Target"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    scans: Mapped[List["Scan"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    reports: Mapped[List["Report"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    assets: Mapped[List["Asset"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )


class Target(BaseModel):
    __tablename__ = "targets"

    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), index=True)
    target: Mapped[str] = mapped_column(String(255))
    target_type: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(50), default="active")

    project: Mapped["Project"] = relationship(back_populates="targets")
    scans: Mapped[List["Scan"]] = relationship(
        back_populates="target", cascade="all, delete-orphan"
    )
    plugin_executions: Mapped[List["PluginExecution"]] = relationship(
        back_populates="target", cascade="all, delete-orphan"
    )


class Scan(BaseModel):
    __tablename__ = "scans"

    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), index=True)
    target_id: Mapped[str] = mapped_column(ForeignKey("targets.id"), index=True)
    scan_type: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(50), default="pending")
    started_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    project: Mapped["Project"] = relationship(back_populates="scans")
    target: Mapped["Target"] = relationship(back_populates="scans")
    findings: Mapped[List["Finding"]] = relationship(
        back_populates="scan", cascade="all, delete-orphan"
    )


class Finding(BaseModel):
    __tablename__ = "findings"

    scan_id: Mapped[str] = mapped_column(ForeignKey("scans.id"), index=True)
    severity: Mapped[SeverityEnum] = mapped_column(Enum(SeverityEnum), index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    evidence: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    scan: Mapped["Scan"] = relationship(back_populates="findings")


class Asset(BaseModel):
    __tablename__ = "assets"

    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), index=True)
    asset_type: Mapped[str] = mapped_column(String(50))
    value: Mapped[str] = mapped_column(String(255))
    source: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    project: Mapped["Project"] = relationship(back_populates="assets")


class Report(BaseModel):
    __tablename__ = "reports"

    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), index=True)
    report_type: Mapped[str] = mapped_column(String(50))
    file_path: Mapped[str] = mapped_column(String(500))
    generated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )

    project: Mapped["Project"] = relationship(back_populates="reports")


class PluginExecution(BaseModel):
    __tablename__ = "plugin_executions"

    plugin_name: Mapped[str] = mapped_column(String(100), index=True)
    target_id: Mapped[str] = mapped_column(ForeignKey("targets.id"), index=True)
    status: Mapped[str] = mapped_column(String(50), default="running")
    started_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    finished_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    output: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    target: Mapped["Target"] = relationship(back_populates="plugin_executions")


class RefreshToken(BaseModel):
    __tablename__ = "refresh_tokens"

    token_id: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    issued_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    expires_at: Mapped[datetime] = mapped_column()
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped["User"] = relationship(back_populates="refresh_tokens")


class Session(BaseModel):
    __tablename__ = "sessions"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    session_id: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    login_time: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    logout_time: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user: Mapped["User"] = relationship(back_populates="sessions")


class AuditLog(BaseModel):
    __tablename__ = "audit_logs"

    user_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("users.id"), index=True, nullable=True
    )
    action: Mapped[str] = mapped_column(String(100), index=True)
    resource: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    ip_address: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    user: Mapped[Optional["User"]] = relationship(back_populates="audit_logs")


class PasswordHistory(BaseModel):
    __tablename__ = "password_history"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    password_hash: Mapped[str] = mapped_column(String(255))

    user: Mapped["User"] = relationship(back_populates="password_history")


class LoginAttempt(BaseModel):
    __tablename__ = "login_attempts"

    username: Mapped[str] = mapped_column(String(255), index=True)
    ip_address: Mapped[str] = mapped_column(String(50))
    timestamp: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    successful: Mapped[bool] = mapped_column(Boolean)


class WorkflowExecution(BaseModel):
    __tablename__ = "workflow_executions"

    workflow_name: Mapped[str] = mapped_column(String(100), index=True)
    status: Mapped[str] = mapped_column(String(50), default="PENDING")
    started_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    finished_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    user_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    target: Mapped[str] = mapped_column(String(255), index=True)
    result_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class AssetRelationship(BaseModel):
    __tablename__ = "asset_relationships"

    parent_asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    child_asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    relationship_type: Mapped[str] = mapped_column(String(50))

    parent_asset: Mapped["Asset"] = relationship(
        "Asset", foreign_keys=[parent_asset_id]
    )
    child_asset: Mapped["Asset"] = relationship("Asset", foreign_keys=[child_asset_id])


class AssetHistory(BaseModel):
    __tablename__ = "asset_history"

    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    timestamp: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    event: Mapped[str] = mapped_column(String(255))

    asset: Mapped["Asset"] = relationship("Asset", foreign_keys=[asset_id])


class AssetTag(BaseModel):
    __tablename__ = "asset_tags"

    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    tag: Mapped[str] = mapped_column(String(50), index=True)

    asset: Mapped["Asset"] = relationship("Asset", foreign_keys=[asset_id])


class IntelligenceRecord(BaseModel):
    __tablename__ = "intelligence_records"

    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    source: Mapped[str] = mapped_column(String(100))
    data: Mapped[str] = mapped_column(Text)
    confidence: Mapped[int] = mapped_column(default=100)

    asset: Mapped["Asset"] = relationship("Asset", foreign_keys=[asset_id])


class ScheduledReport(BaseModel):
    __tablename__ = "scheduled_reports"

    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), index=True)
    report_type: Mapped[str] = mapped_column(String(50))
    frequency: Mapped[str] = mapped_column(String(50))
    last_run: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    next_run: Mapped[Optional[datetime]] = mapped_column(nullable=True)


class DashboardSnapshot(BaseModel):
    __tablename__ = "dashboard_snapshots"

    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), index=True)
    timestamp: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    metrics_json: Mapped[str] = mapped_column(Text)
