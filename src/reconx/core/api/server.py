from reconx.core.database.db import DatabaseManager
# Scaffold for FastAPI
class ReconXAPI:
    def __init__(self):
        self.db = DatabaseManager()

    def get_assets(self):
        return self.db.query_assets()

    def get_findings(self):
        return self.db.query_findings()
