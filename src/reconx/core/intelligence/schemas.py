from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional, Literal
from reconx.core.validation.validators import validate_domain, validate_ip, validate_url
from reconx.core.exceptions.errors import ValidationError

class AssetSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    asset_type: Literal["DOMAIN", "SUBDOMAIN", "IP", "URL", "ENDPOINT"]
    value: str
    source: str = "unknown"
    project_id: str

    @field_validator("value")
    @classmethod
    def validate_asset_value(cls, v: str, info) -> str:
        asset_type = info.data.get("asset_type")
        try:
            if asset_type in ("DOMAIN", "SUBDOMAIN"):
                return validate_domain(v)
            elif asset_type == "IP":
                return validate_ip(v)
            elif asset_type in ("URL", "ENDPOINT"):
                return validate_url(v)
        except ValidationError as e:
            raise ValueError(f"Invalid asset value for type {asset_type}: {e}")
        return v

class FindingSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    finding_type: str
    severity: Literal["INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"]
    description: str
    asset_value: str
    source: str = "unknown"

