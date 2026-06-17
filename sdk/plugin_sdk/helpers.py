import asyncio
from typing import List
from .exceptions import PluginExecutionError


async def run_command(cmd: List[str]) -> str:
    """
    Helper function to securely execute a CLI command using asyncio.subprocess.
    """
    process = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        raise PluginExecutionError(
            f"Command failed with code {process.returncode}: {stderr.decode()}"
        )

    return stdout.decode()
