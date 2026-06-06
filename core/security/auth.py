import time
import base64
import json
from typing import Dict, Optional

class AuthSystem:
    def __init__(self):
        # In-memory mock database for MVP
        self.users = {
            "admin1": {"password": "password123", "role": "ADMIN"},
            "analyst1": {"password": "password123", "role": "ANALYST"},
            "viewer1": {"password": "password123", "role": "VIEWER"}
        }
        
    def login(self, username: str, password: str) -> Optional[str]:
        if username in self.users and self.users[username]["password"] == password:
            role = self.users[username]["role"]
            return self._generate_mock_jwt(username, role)
        return None

    def _generate_mock_jwt(self, username: str, role: str) -> str:
        """Generates a base64 encoded token simulating a JWT."""
        payload = {
            "sub": username,
            "role": role,
            "exp": int(time.time()) + 3600
        }
        payload_str = json.dumps(payload)
        return base64.b64encode(payload_str.encode()).decode()

    def decode_token(self, token: str) -> Optional[Dict]:
        try:
            payload_str = base64.b64decode(token).decode()
            payload = json.loads(payload_str)
            if payload["exp"] < time.time():
                return None # Expired
            return payload
        except:
            return None

auth_system = AuthSystem()
