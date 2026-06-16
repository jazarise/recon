from reconx.core.models import Relationship, RelationshipType

class RelationshipNormalizer:
    @staticmethod
    def link_assets(source_id: str, target_id: str, rel_type: RelationshipType) -> Relationship:
        return Relationship(
            source_id=source_id,
            target_id=target_id,
            type=rel_type
        )
