import requests


class HttpClient:
    """Canonical Unified HTTP Client, preventing duplicate request wrappers."""

    @staticmethod
    def get(url: str, headers: dict = None, timeout: int = 10) -> dict:
        """Standard GET request wrapper returning clean status and body."""
        try:
            resp = requests.get(url, headers=headers, timeout=timeout)
            return {
                "url": url,
                "status_code": resp.status_code,
                "headers": dict(resp.headers),
                "text": resp.text,
                "error": None,
            }
        except Exception as e:
            return {
                "url": url,
                "status_code": 0,
                "headers": {},
                "text": "",
                "error": str(e),
            }

    @staticmethod
    def post(
        url: str, json: dict = None, headers: dict = None, timeout: int = 10
    ) -> dict:
        try:
            resp = requests.post(url, json=json, headers=headers, timeout=timeout)
            return {
                "url": url,
                "status_code": resp.status_code,
                "headers": dict(resp.headers),
                "text": resp.text,
                "json": resp.json() if resp.text else None,
                "error": None,
            }
        except Exception as e:
            return {
                "url": url,
                "status_code": 0,
                "headers": {},
                "text": "",
                "json": None,
                "error": str(e),
            }

    @staticmethod
    def request(method: str, url: str, headers: dict = None, timeout: int = 10) -> dict:
        try:
            resp = requests.request(method, url, headers=headers, timeout=timeout)
            return {
                "url": url,
                "status_code": resp.status_code,
                "headers": dict(resp.headers),
                "text": resp.text,
                "error": None,
            }
        except Exception as e:
            return {
                "url": url,
                "status_code": 0,
                "headers": {},
                "text": "",
                "error": str(e),
            }
