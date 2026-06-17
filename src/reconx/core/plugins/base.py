from pydantic import BaseModel
from typing import List, Any, Dict
from reconx.core.plugins.permissions import PluginPermission
from abc import ABC, abstractmethod


class PluginResult(BaseModel):
    status: str
    findings: List[Dict[str, Any]] = []
    assets: List[Dict[str, Any]] = []
    logs: List[str] = []
    errors: List[str] = []


class ReconXPlugin(ABC):
    name: str = ""
    version: str = ""
    author: str = ""
    description: str = ""
    category: str = ""
    requires: List[str] = []
    permissions: List[PluginPermission] = []

    async def validate(self) -> bool:
        """Validate if the plugin can run"""
        return True

    @abstractmethod
    async def execute(self, target: str) -> PluginResult:
        """Execute the plugin on the given target"""
        pass

    async def cleanup(self) -> None:
        """Cleanup after execution"""
        pass
