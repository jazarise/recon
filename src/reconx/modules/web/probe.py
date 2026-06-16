import uuid
from typing import Any
from core.models import AdapterResult, Asset, AssetType
from modules.base_module import BaseNativeModule
from core.utils.http_client import HttpClient

class NativeWebProbe(BaseNativeModule):
    def run(self, target: str) -> Any:
        if not target.startswith("http"):
            target = f"http://{target}"
        return HttpClient.get(target)

    def normalize(self, raw_data: Any) -> AdapterResult:
        result = AdapterResult()
        if raw_data.get("status_code", 0) > 0:
            result.assets.append(Asset(
                id=str(uuid.uuid4()),
                type=AssetType.URL,
                value=raw_data["url"],
                source="native.web.probe",
                confidence=1.0
            ))
        return result
