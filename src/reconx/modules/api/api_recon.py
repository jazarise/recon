import uuid
from reconx.modules.base_module import BaseNativeModule
from reconx.core.models import AdapterResult, Asset, AssetType, Relationship, RelationshipType
from reconx.modules.api.schema_inference import schema_inference_engine
from reconx.modules.api.graphql_engine import graphql_engine
from reconx.modules.api.probe_engine import probe_engine
from reconx.modules.api.classifier import api_classifier

class NativeApiRecon(BaseNativeModule):
    @property
    def capability_name(self) -> str:
        return "discovery.api"

    def run(self, target: str, **kwargs) -> AdapterResult:
        res = AdapterResult()
        print(f"[*] Starting API Intelligence Recon on {target}...")
        
        domain_asset = Asset(
            id=str(uuid.uuid4()),
            type=AssetType.DOMAIN,
            value=target,
            source="native.discovery.api",
            confidence=1.0
        )
        res.assets.append(domain_asset)
        
        # 1. Look for OpenAPI/Swagger
        openapi_data = schema_inference_engine.discover_openapi(target)
        if openapi_data:
            openapi_asset = Asset(
                id=str(uuid.uuid4()),
                type=AssetType.OPENAPI_SPEC,
                value=openapi_data["endpoint"],
                source="native.discovery.api",
                confidence=1.0
            )
            res.assets.append(openapi_asset)
            res.relationships.append(Relationship(
                source_id=domain_asset.id,
                target_id=openapi_asset.id,
                type=RelationshipType.EXPOSES
            ))
            
            # Extract endpoints from OpenAPI spec
            spec = openapi_data.get("spec", {})
            paths = spec.get("paths", {})
            for path in paths.keys():
                ep_asset = Asset(
                    id=str(uuid.uuid4()),
                    type=AssetType.API_ENDPOINT,
                    value=f"{target.rstrip('/')}{path}",
                    source="native.discovery.api",
                    confidence=1.0
                )
                res.assets.append(ep_asset)
                res.relationships.append(Relationship(
                    source_id=openapi_asset.id,
                    target_id=ep_asset.id,
                    type=RelationshipType.EXPOSES
                ))
                
        # 2. Look for GraphQL
        graphql_data = graphql_engine.introspect(target)
        if graphql_data:
            graphql_asset = Asset(
                id=str(uuid.uuid4()),
                type=AssetType.GRAPHQL_SCHEMA,
                value=graphql_data["endpoint"],
                source="native.discovery.api",
                confidence=1.0
            )
            res.assets.append(graphql_asset)
            res.relationships.append(Relationship(
                source_id=domain_asset.id,
                target_id=graphql_asset.id,
                type=RelationshipType.EXPOSES
            ))
            
        # 3. Probe existing endpoints (Mock list or passed in via kwargs in real system)
        # For this execution, let's probe a standard /api/admin to demo the engine
        endpoints_to_probe = [f"{target.rstrip('/')}/api/admin"]
        
        for ep in endpoints_to_probe:
            probe_results = probe_engine.probe_endpoint(target, ep)
            classification = api_classifier.classify(probe_results)
            
            ep_asset = Asset(
                id=str(uuid.uuid4()),
                type=AssetType.API_ENDPOINT,
                value=ep,
                source="native.discovery.api",
                confidence=0.9
            )
            res.assets.append(ep_asset)
            res.relationships.append(Relationship(
                source_id=domain_asset.id,
                target_id=ep_asset.id,
                type=RelationshipType.EXPOSES
            ))
            
            # Map the Authentication requirement based on classification
            auth_asset = Asset(
                id=str(uuid.uuid4()),
                type=AssetType.AUTH_METHOD,
                value=classification,
                source="native.discovery.api",
                confidence=0.9
            )
            res.assets.append(auth_asset)
            res.relationships.append(Relationship(
                source_id=ep_asset.id,
                target_id=auth_asset.id,
                type=RelationshipType.USES
            ))
            
        return res

    def normalize(self, raw_data: AdapterResult) -> AdapterResult:
        return raw_data
