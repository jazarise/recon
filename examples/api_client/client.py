import requests

response = requests.post(
    "http://localhost:8000/api/scans", json={"target": "example.com"}
)
print(response.json())
