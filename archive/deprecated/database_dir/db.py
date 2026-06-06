import sqlite3
import json
from pathlib import Path
from core.schemas import HostProfile, OrganizationProfile, CorrelatedFinding

class DatabaseManager:
    def __init__(self, workspace="default"):
        self.workspace = workspace
        self.db_path = Path(f"workspaces/{workspace}/reconx.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self._init_db()

    def _init_db(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS assets (id TEXT PRIMARY KEY, type TEXT, data TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        c.execute('''CREATE TABLE IF NOT EXISTS findings (id TEXT PRIMARY KEY, severity TEXT, data TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        c.execute('''CREATE TABLE IF NOT EXISTS organizations (name TEXT PRIMARY KEY, data TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        c.execute('''CREATE TABLE IF NOT EXISTS knowledge_nodes (id TEXT PRIMARY KEY, type TEXT, data TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS knowledge_edges (source TEXT, target TEXT, relation TEXT)''')
        self.conn.commit()

    def save_organization(self, profile: OrganizationProfile):
        c = self.conn.cursor()
        c.execute("INSERT OR REPLACE INTO organizations (name, data) VALUES (?, ?)", 
                  (profile.organization, profile.model_dump_json()))
        
        # Save nested assets
        for domain in profile.domains:
            c.execute("INSERT OR REPLACE INTO assets (id, type, data) VALUES (?, ?, ?)",
                      (domain.domain, "domain", domain.model_dump_json()))
            for vuln in domain.vulnerabilities:
                vuln_id = f"{domain.domain}_{vuln.type}"
                c.execute("INSERT OR REPLACE INTO findings (id, severity, data) VALUES (?, ?, ?)",
                          (vuln_id, vuln.severity.value, vuln.model_dump_json()))
        self.conn.commit()

    def query_findings(self, severity_filter=None):
        c = self.conn.cursor()
        if severity_filter:
            c.execute("SELECT data FROM findings WHERE severity=?", (severity_filter,))
        else:
            c.execute("SELECT data FROM findings")
        return [json.loads(row[0]) for row in c.fetchall()]

    def query_assets(self):
        c = self.conn.cursor()
        c.execute("SELECT data FROM assets")
        return [json.loads(row[0]) for row in c.fetchall()]
        
    def save_knowledge_node(self, node_id, node_type, data):
        c = self.conn.cursor()
        c.execute("INSERT OR REPLACE INTO knowledge_nodes (id, type, data) VALUES (?, ?, ?)", (node_id, node_type, json.dumps(data)))
        self.conn.commit()
