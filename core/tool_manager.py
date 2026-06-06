import shutil
from typing import Optional

class ToolManager:
    @staticmethod
    def get(tool_name: str) -> Optional[str]:
        # Simple lookup using shutil.which for PATH binaries
        # In a real environment, this might check custom directories
        return shutil.which(tool_name)
    
    @staticmethod
    def is_installed(tool_name: str) -> bool:
        return ToolManager.get(tool_name) is not None
