import ipaddress
from typing import List
from core.reconx.utils.logger import logger

class SecuritySandbox:
    """Provides security boundaries and validation for ReconX execution."""
    
    def __init__(self, allowed_scopes: List[str]):
        self.allowed_scopes = allowed_scopes

    def is_target_in_scope(self, target: str) -> bool:
        """Validate if a target IP/domain is within allowed scopes."""
        if not self.allowed_scopes:
            logger.warning("No allowed scopes defined. All targets blocked by default.")
            return False

        try:
            # Check if target is an IP
            ip = ipaddress.ip_address(target)
            for scope in self.allowed_scopes:
                try:
                    network = ipaddress.ip_network(scope)
                    if ip in network:
                        return True
                except ValueError:
                    pass
        except ValueError:
            # Target is a domain, we might need to resolve it or just string match
            for scope in self.allowed_scopes:
                if target == scope or target.endswith(f".{scope}"):
                    return True
                    
        return False

    def validate_plugin_capabilities(self, capabilities: List[str]) -> bool:
        """Ensure the plugin doesn't request dangerous capabilities."""
        banned_capabilities = ["exploit", "credential_harvesting", "persistence"]
        for cap in capabilities:
            if cap in banned_capabilities:
                logger.error(f"Plugin requested banned capability: {cap}")
                return False
        return True
