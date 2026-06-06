from core.database.models import DBRelationship
from sqlalchemy.orm import Session

def add_relationship(db: Session, source: str, relation: str, target: str):
    rel = DBRelationship(source=source, relation=relation, target=target)
    db.add(rel)
    db.commit()
    db.refresh(rel)
    return rel
