from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone
from enum import Enum

class Severity(str, Enum):
    INFO = "Info"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class Confidence(str, Enum):
    VERY_HIGH = "Very High"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    UNKNOWN = "Unknown"

# Asset Lifecycle
class AssetLifecycle(BaseModel):
    first_seen: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_seen: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    current_status: str = "active"
    ownership: str = "unknown"

class FindingLifecycle(BaseModel):
    status: str = "Open"
    comments: List[str] = Field(default_factory=list)
    assignments: str = "unassigned"

# Technical Assets
class Asset(BaseModel):
    type: str
    value: str
    tags: List[str] = Field(default_factory=list)
    lifecycle: AssetLifecycle = Field(default_factory=AssetLifecycle)

class Domain(BaseModel):
    value: str
    source: str = "unknown"
    lifecycle: AssetLifecycle = Field(default_factory=AssetLifecycle)

class IPAddress(BaseModel):
    value: str
    source: str = "unknown"
    lifecycle: AssetLifecycle = Field(default_factory=AssetLifecycle)

class DNSRecord(BaseModel):
    type: str
    value: str

class Port(BaseModel):
    number: int
    protocol: str = "tcp"
    state: str = "open"

class Technology(BaseModel):
    name: str
    version: Optional[str] = None

class URL(BaseModel):
    value: str
    status_code: Optional[int] = None
    title: Optional[str] = None
    technologies: List[str] = Field(default_factory=list)

class Endpoint(BaseModel):
    path: str
    source: str = "unknown"

class Parameter(BaseModel):
    name: str
    source: str = "unknown"

class Evidence(BaseModel):
    request: Optional[str] = None
    response: Optional[str] = None
    extracted_data: Optional[Dict[str, Any]] = None
    screenshots: List[str] = Field(default_factory=list)
    evidence_path: Optional[str] = None

class Finding(BaseModel):
    id: str
    type: str
    severity: Severity = Severity.INFO
    url: Optional[str] = None
    description: Optional[str] = None
    asset: str
    evidence: Optional[Evidence] = None
    tags: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    lifecycle: FindingLifecycle = Field(default_factory=FindingLifecycle)

class Vulnerability(BaseModel):
    type: str
    severity: Severity = Severity.INFO
    url: str
    evidence: Optional[Evidence] = None
    lifecycle: FindingLifecycle = Field(default_factory=FindingLifecycle)

# OSINT & Intelligence Assets
class Employee(BaseModel):
    name: str
    role: Optional[str] = None
    confidence: Confidence = Confidence.UNKNOWN

class Email(BaseModel):
    value: str
    employee_name: Optional[str] = None
    source: str = "unknown"
    confidence: Confidence = Confidence.UNKNOWN

class Username(BaseModel):
    value: str
    source: str = "unknown"
    confidence: Confidence = Confidence.UNKNOWN

class PhoneNumber(BaseModel):
    value: str
    source: str = "unknown"
    confidence: Confidence = Confidence.UNKNOWN

class SocialProfile(BaseModel):
    platform: str
    url: str
    username: str
    confidence: Confidence = Confidence.UNKNOWN

class Exposure(BaseModel):
    type: str
    description: str
    source: str = "unknown"
    confidence: Confidence = Confidence.UNKNOWN

class BreachRecord(BaseModel):
    source: str
    exposure_type: str
    exposure_date: Optional[str] = None
    confidence: Confidence = Confidence.UNKNOWN

class ThreatIndicator(BaseModel):
    indicator_type: str
    value: str
    malicious: bool = True
    source: str = "unknown"
    confidence: Confidence = Confidence.UNKNOWN

# --- AI Data Layer Models ---
class RiskAssessment(BaseModel):
    score: float
    severity: Severity
    factors: List[str] = Field(default_factory=list)

class DeduplicatedFinding(BaseModel):
    finding_type: str
    targets: List[str] = Field(default_factory=list)
    sources: List[str] = Field(default_factory=list)
    confidence: Confidence = Confidence.UNKNOWN

class CorrelatedFinding(BaseModel):
    target: str
    findings: List[str] = Field(default_factory=list)
    confidence: Confidence = Confidence.UNKNOWN
    risk: Optional[RiskAssessment] = None
    deduplicated_findings: List[DeduplicatedFinding] = Field(default_factory=list)

class AttackSurfaceProfile(BaseModel):
    total_hosts: int = 0
    live_services: int = 0
    exposed_endpoints: int = 0
    critical_vulnerabilities: int = 0
    total_exposures: int = 0

class AIExecutiveSummary(BaseModel):
    overview: str
    key_risks: List[str] = Field(default_factory=list)
    attack_surface: AttackSurfaceProfile
    recommended_actions: List[str] = Field(default_factory=list)

class AITechnicalSummary(BaseModel):
    correlated_findings: List[CorrelatedFinding] = Field(default_factory=list)
    explanations: Dict[str, str] = Field(default_factory=dict)

# Profiles
class HostProfile(BaseModel):
    domain: Optional[str] = None
    ip: Optional[str] = None
    ports: List[int] = Field(default_factory=list)
    technologies: List[str] = Field(default_factory=list)
    urls: List[str] = Field(default_factory=list)
    dns_records: List[DNSRecord] = Field(default_factory=list)
    endpoints: List[Endpoint] = Field(default_factory=list)
    parameters: List[Parameter] = Field(default_factory=list)
    findings: List[Finding] = Field(default_factory=list)
    vulnerabilities: List[Vulnerability] = Field(default_factory=list)

class OrganizationProfile(BaseModel):
    organization: str
    domains: List[HostProfile] = Field(default_factory=list)
    employees: List[Employee] = Field(default_factory=list)
    emails: List[Email] = Field(default_factory=list)
    usernames: List[Username] = Field(default_factory=list)
    phone_numbers: List[PhoneNumber] = Field(default_factory=list)
    social_profiles: List[SocialProfile] = Field(default_factory=list)
    exposures: List[Exposure] = Field(default_factory=list)
    breach_records: List[BreachRecord] = Field(default_factory=list)
    threat_indicators: List[ThreatIndicator] = Field(default_factory=list)
    ai_executive_summary: Optional[AIExecutiveSummary] = None
    ai_technical_summary: Optional[AITechnicalSummary] = None

class Organization(BaseModel):
    name: str
    domain: str

# Knowledge Graph Models
class KnowledgeNode(BaseModel):
    id: str
    type: str # 'Organization', 'Domain', 'Host', 'Finding'
    properties: Dict[str, Any] = Field(default_factory=dict)

class KnowledgeRelationship(BaseModel):
    source_id: str
    target_id: str
    relation_type: str # 'owns', 'hosts', 'exposes'
