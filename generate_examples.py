examples = {
    "examples/basic_workflow/workflow.yaml": """name: basic
description: A basic workflow
stages:
  - id: scan
    plugin: basic_plugin
""",
    "examples/advanced_workflow/workflow.yaml": """name: advanced
description: Complex multi-stage workflow
stages:
  - id: enum
    plugin: subfinder
  - id: scan
    plugin: nuclei
    depends_on: [enum]
""",
    "examples/custom_plugin/plugin.py": """from reconx.core.plugins import ReconPlugin

class CustomPlugin(ReconPlugin):
    async def execute(self, target):
        return {"status": "success"}
""",
    "examples/api_client/client.py": """import requests

response = requests.post("http://localhost:8000/api/scans", json={"target": "example.com"})
print(response.json())
""",
    "examples/docker_deployment/docker-compose.yml": """version: '3.8'
services:
  reconx:
    image: reconx/reconx:latest
    ports:
      - "8000:8000"
""",
}

for path, content in examples.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
