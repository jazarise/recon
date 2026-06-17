import sqlite3
import json
import logging

logger = logging.getLogger("reconx")


class DatabaseLayer:
    def __init__(self, db_path="reconx.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS campaigns (
                id TEXT PRIMARY KEY,
                target TEXT,
                status TEXT,
                results TEXT
            )
        """)
        conn.commit()
        conn.close()

    def save_campaign(self, campaign_id: str, target: str, status: str, results: dict):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "REPLACE INTO campaigns (id, target, status, results) VALUES (?, ?, ?, ?)",
            (campaign_id, target, status, json.dumps(results)),
        )
        conn.commit()
        conn.close()

    def get_campaign(self, campaign_id: str) -> dict:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT target, status, results FROM campaigns WHERE id=?", (campaign_id,)
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            return {"target": row[0], "status": row[1], "results": json.loads(row[2])}
        return None
