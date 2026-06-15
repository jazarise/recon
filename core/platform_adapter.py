import platform
import shutil
import subprocess
from pathlib import Path
from typing import Optional, Tuple

class PlatformAdapter:
    """
    OS-agnostic compatibility layer for ReconX.
    Ensures safe execution and path resolution across Linux, Windows, and macOS.
    """
    
    @staticmethod
    def detect_os() -> str:
        """Returns lowercase OS name: linux, windows, or darwin."""
        sys_name = platform.system().lower()
        if sys_name not in ["linux", "windows", "darwin"]:
            return "linux" # default fallback
        return sys_name

    @staticmethod
    def resolve_path(path_str: str) -> Path:
        """
        Safely resolves a path string across operating systems.
        Expands ~ to the user's home directory.
        If a hardcoded windows path (C:\\ or E:\\) is given on Linux, it remaps to ~/ReconX.
        """
        if PlatformAdapter.detect_os() != "windows":
            if path_str.startswith("C:\\") or path_str.startswith("E:\\"):
                # Remap bad hardcoded Windows paths to standard Linux home
                parts = path_str.replace("\\", "/").split("/")
                # Extract trailing parts after ReconX if possible, else just use root
                return Path.home() / "ReconX" / parts[-1]
        
        p = Path(path_str).expanduser()
        return p.resolve()

    @staticmethod
    def dependency_check(binary_name: str) -> bool:
        """Check if a binary exists in the system PATH."""
        return shutil.which(binary_name) is not None

    @staticmethod
    def shell_execute(command: list, cwd: Optional[Path] = None) -> Tuple[int, str, str]:
        """
        Execute a shell command safely across platforms.
        Returns (return_code, stdout, stderr).
        """
        try:
            cwd_str = str(cwd) if cwd else None
            result = subprocess.run(
                command, 
                cwd=cwd_str,
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True,
                check=False
            )
            return result.returncode, result.stdout, result.stderr
        except Exception as e:
            return 1, "", str(e)
