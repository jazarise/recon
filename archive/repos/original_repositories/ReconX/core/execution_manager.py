"""
ReconX ExecutionManager — orchestrates individual step execution
using isolated subprocesses for sandboxed plugin execution.
"""

import sys
import json
import asyncio
from pathlib import Path
from typing import Any, Dict, Optional
from core.secrets_manager import SecretsManager
from core.paths import PROJECT_ROOT

class ExecutionManager:
    """Manage the execution of individual workflow steps using isolated subprocesses."""

    def __init__(self, event_bus: Any, plugin_loader: Any = None) -> None:
        self.event_bus = event_bus
        self.plugin_loader = plugin_loader
        self.secrets_manager = SecretsManager()
        self._runner_path = str(PROJECT_ROOT / "core" / "subprocess_runner.py")

    async def execute_step(self, step: Dict[str, Any], target: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a single workflow *step* in an isolated subprocess."""
        if context is None:
            context = {"target": target}
            
        step_id = step.get("id", "unknown")
        plugin_name = step.get("plugin", "unknown")
        plugin_path = step.get("plugin_path", "")
        timeout = step.get("timeout", 300)
        config = step.get("config", step.get("args", {}))

        await self.event_bus.publish("task.started", {
            "step_id": step_id,
            "plugin": plugin_name,
            "target": target,
        })
        
        await self.event_bus.publish("plugin_started", {
            "plugin": plugin_name,
            "target": target,
        })

        if not plugin_path:
            await self.event_bus.publish("plugin_failed", {"plugin": plugin_name, "error": "No plugin_path provided"})
            raise ValueError(f"No plugin_path provided for step {step_id}")

        await self.event_bus.publish("plugin_progress", {"plugin": plugin_name, "message": "Spawning isolated subprocess"})

        # Prepare payload
        payload = {
            "plugin_path": plugin_path,
            "config": config,
            "context": context
        }
        payload_bytes = json.dumps(payload).encode("utf-8")

        # Prepare environment with secrets
        env = self.secrets_manager.get_plugin_environment(plugin_name)

        # Spawn subprocess
        process = await asyncio.create_subprocess_exec(
            sys.executable, self._runner_path,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env
        )

        try:
            # Enforce hard timeout
            stdout, stderr = await asyncio.wait_for(
                process.communicate(input=payload_bytes),
                timeout=timeout
            )
            
            stdout_text = stdout.decode("utf-8").strip()
            stderr_text = stderr.decode("utf-8").strip()
            
            # Try parsing result first, as runner puts structured errors in stdout
            result_wrapper = {}
            if stdout_text:
                try:
                    result_wrapper = json.loads(stdout_text)
                except json.JSONDecodeError:
                    pass
                    
            if process.returncode != 0:
                if result_wrapper and result_wrapper.get("status") == "error":
                    raise RuntimeError(result_wrapper.get("error", "Unknown plugin error"))
                error_msg = stderr_text or stdout_text or "Unknown subprocess failure"
                raise RuntimeError(f"Subprocess failed with code {process.returncode}: {error_msg}")

            if result_wrapper.get("status") == "error":
                raise RuntimeError(result_wrapper.get("error", "Unknown plugin error"))
            
            if not result_wrapper:
                raise RuntimeError(f"Failed to parse plugin output. Raw: {stdout_text[:200]}")
                
            result = result_wrapper.get("data", {})

            await self.event_bus.publish("plugin_completed", {
                "plugin": plugin_name,
                "status": "completed",
            })
            await self.event_bus.publish("task.completed", {
                "step_id": step_id,
                "plugin": plugin_name,
                "status": "completed",
            })
            return result

        except asyncio.TimeoutError:
            try:
                process.kill()
            except OSError:
                pass
            error_msg = f"Step '{step_id}' timed out after {timeout}s and was forcibly terminated."
            await self.event_bus.publish("plugin_failed", {
                "plugin": plugin_name,
                "error": error_msg,
            })
            await self.event_bus.publish("task.failed", {
                "step_id": step_id,
                "plugin": plugin_name,
                "error": error_msg,
            })
            raise RuntimeError(error_msg)

        except Exception as exc:
            try:
                if process.returncode is None:
                    process.kill()
            except OSError:
                pass
            await self.event_bus.publish("plugin_failed", {
                "plugin": plugin_name,
                "error": str(exc),
            })
            await self.event_bus.publish("task.failed", {
                "step_id": step_id,
                "plugin": plugin_name,
                "error": str(exc),
            })
            raise
