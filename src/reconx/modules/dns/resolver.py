import uuid
from typing import Any
from reconx.core.models import AdapterResult, Asset, AssetType
from reconx.modules.base_module import BaseNativeModule
from reconx.core.utils.dns_client import DnsClient

class NativeDnsResolver(BaseNativeModule):
    def run(self, target: str) -> Any:
        return DnsClient.resolve_a(target)

    def normalize(self, raw_data: Any) -> AdapterResult:
        result = AdapterResult()
        for ip in raw_data:
            result.assets.append(Asset(
                id=str(uuid.uuid4()),
                type=AssetType.IP_ADDRESS,
                value=ip,
                source="native.dns.resolver",
                confidence=1.0
            ))
        return result
