from core.database.session import SessionLocal
from core.database.models import DBFinding

class SearchEngine:
    def search(self, query: str):
        db = SessionLocal()
        search_pattern = f"%{query}%"
        results = db.query(DBFinding).filter(
            DBFinding.value.ilike(search_pattern) | 
            DBFinding.category.ilike(search_pattern) | 
            DBFinding.source.ilike(search_pattern)
        ).all()
        db.close()
        return results

search_engine = SearchEngine()
