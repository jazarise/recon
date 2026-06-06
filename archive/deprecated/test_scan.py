import asyncio
import sys
from pathlib import Path
from core.project_manager import ProjectManager
from reconx import _run_workflow

async def main():
    pm = ProjectManager()
    try:
        pm.create_project("test_proj", "example.com", "test", [])
        print("Project created successfully.")
    except FileExistsError:
        print("Project already exists.")

    print("Initiating scan...")
    result = await _run_workflow("basic.yaml", "example.com", "test_proj")
    if result:
        print("Scan initiated without crash.")
    else:
        print("Scan failed.")

if __name__ == "__main__":
    asyncio.run(main())
