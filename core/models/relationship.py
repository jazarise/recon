import uuid
from pydantic import BaseModel, Field
from .enums import RelationshipType

class Relationship(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source_id: str
    target_id: str
    type: RelationshipType
