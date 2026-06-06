from typing import Dict, Type
from modules.base_module import BaseNativeModule

from modules.discovery.subdomains import NativeSubdomainDiscovery
from modules.dns.resolver import NativeDnsResolver
from modules.web.probe import NativeWebProbe
from modules.osint.email import NativeOsintEmail

# The absolute source of truth mapping a Capability -> 1 Canonical Native Module
NATIVE_MODULES_REGISTRY: Dict[str, Type[BaseNativeModule]] = {
    "discovery.subdomains": NativeSubdomainDiscovery,
    "dns.resolve": NativeDnsResolver,
    "web.probe": NativeWebProbe,
    "osint.email": NativeOsintEmail
}

def get_native_module(capability: str) -> BaseNativeModule:
    """Returns the single canonical native module instance for a capability, or None if it relies purely on plugins."""
    module_class = NATIVE_MODULES_REGISTRY.get(capability)
    return module_class() if module_class else None
