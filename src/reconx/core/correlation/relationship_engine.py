from typing import List
from reconx.core.models import Relationship, RelationshipType
from reconx.core.normalization import RelationshipNormalizer

class RelationshipEngine:
    """Manages the creation and deduplication of relationships."""

    def __init__(self):
        self.relationships: List[Relationship] = []
        self._seen_sigs = set()

    def add_relationship(self, source_id: str, target_id: str, rel_type: RelationshipType):
        """Adds a relationship if it doesn't already exist."""
        sig = f"{source_id}::{rel_type.value}::{target_id}"
        if sig not in self._seen_sigs:
            self._seen_sigs.add(sig)
            rel = RelationshipNormalizer.link_assets(source_id, target_id, rel_type)
            self.relationships.append(rel)

    def get_all(self) -> List[Relationship]:
        return self.relationships
