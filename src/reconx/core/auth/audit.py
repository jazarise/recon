from datetime import datetime
import sqlite3
from pathlib import Path


class AuditLogger:
    def __init__(self, workspace="default"):
        self.db_path = Path(f"workspaces/{workspace}/audit.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self._init_db()

    def _init_db(self):
        c = self.conn.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS audit_log (timestamp DATETIME, user TEXT, action TEXT, result TEXT)"""
        )
        self.conn.commit()

    def log(self, user: str, action: str, result: str):
        c = self.conn.cursor()
        c.execute(
            "INSERT INTO audit_log VALUES (?, ?, ?, ?)",
            (datetime.now(), user, action, result),
        )
        self.conn.commit()
