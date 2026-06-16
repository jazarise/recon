import uuid
from modules.base_module import BaseNativeModule
from core.models import AdapterResult, Asset, AssetType, Relationship, RelationshipType
from modules.javascript.collector import js_collector
from modules.javascript.endpoint_extractor import endpoint_extractor
from modules.javascript.secret_detector import secret_detector

class NativeJsRecon(BaseNativeModule):
    @property
    def capability_name(self) -> str:
        return "discovery.javascript"

    def run(self, target: str, **kwargs) -> AdapterResult:
        res = AdapterResult()
        print(f"[*] Starting JS Recon on {target}...")
        
        # 1. Collect JS
        js_data = js_collector.collect(target)
        
        # Create base domain asset
        domain_asset = Asset(
            id=str(uuid.uuid4()),
            type=AssetType.DOMAIN,
            value=target,
            source="native.discovery.javascript",
            confidence=1.0
        )
        res.assets.append(domain_asset)
        
        for url, content in js_data.items():
            # Create JS_FILE asset
            js_asset = Asset(
                id=str(uuid.uuid4()),
                type=AssetType.JS_FILE,
                value=url,
                source="native.discovery.javascript",
                confidence=1.0
            )
            res.assets.append(js_asset)
            
            # Relate Domain -> JS_FILE
            rel1 = Relationship(
                source_id=domain_asset.id,
                target_id=js_asset.id,
                type=RelationshipType.HOSTS
            )
            res.relationships.append(rel1)
            
            # 2. Extract Endpoints
            endpoints = endpoint_extractor.extract(content)
            for ep in endpoints:
                ep_asset = Asset(
                    id=str(uuid.uuid4()),
                    type=AssetType.API_ENDPOINT,
                    value=ep,
                    source="native.discovery.javascript",
                    confidence=0.9
                )
                res.assets.append(ep_asset)
                
                # Relate JS_FILE -> API_ENDPOINT
                rel2 = Relationship(
                    source_id=js_asset.id,
                    target_id=ep_asset.id,
                    type=RelationshipType.EXPOSES
                )
                res.relationships.append(rel2)
                
            # 3. Detect Secrets
            secrets = secret_detector.detect(content)
            for sec in secrets:
                sec_asset = Asset(
                    id=str(uuid.uuid4()),
                    type=AssetType.SECRET,
                    value=f"{sec['type']}:{sec['value']}",
                    source="native.discovery.javascript",
                    confidence=1.0
                )
                res.assets.append(sec_asset)
                
                # Relate JS_FILE -> SECRET
                rel3 = Relationship(
                    source_id=js_asset.id,
                    target_id=sec_asset.id,
                    type=RelationshipType.EXPOSES
                )
                res.relationships.append(rel3)
                
        return res

    def normalize(self, raw_data: AdapterResult) -> AdapterResult:
        return raw_data
