from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Dict, Any, List
from reconx.core.database.models import Asset, AssetRelationship, AssetHistory
from reconx.core.intelligence.deduplicator import Deduplicator
from reconx.core.intelligence.relationship_engine import RelationshipEngine
from reconx.core.intelligence.asset_correlator import AssetCorrelator


from reconx.core.intelligence.schemas import AssetSchema
from pydantic import ValidationError

class IntelligenceStore:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def ingest_plugin_result(self, project_id: str, results: Dict[str, Any]):
        # Pipeline: Normalizer -> Deduplicator -> Relationship -> Intelligence Store
        raw_assets = results.get("assets", [])
        raw_findings = results.get("findings", [])

        normalized_assets = []
        for a in raw_assets:
            try:
                asset = AssetSchema(
                    asset_type=a.get("type", a.get("asset_type", "DOMAIN")).upper(),
                    value=a.get("value", ""),
                    source=a.get("source", "unknown"),
                    project_id=project_id,
                )
                normalized_assets.append(asset.model_dump())
            except ValidationError as e:
                # Log invalid asset (silently ignore for now as per legacy behavior)
                continue

        deduped_assets = Deduplicator.deduplicate_assets(normalized_assets)

        # Save assets
        asset_id_map = {}
        for a in deduped_assets:
            # check if exists
            res = await self.db.execute(
                select(Asset).filter(
                    Asset.project_id == project_id,
                    Asset.asset_type == a["asset_type"],
                    Asset.value == a["value"],
                )
            )
            existing = res.scalars().first()
            if not existing:
                new_asset = Asset(
                    project_id=project_id,
                    asset_type=a["asset_type"],
                    value=a["value"],
                    source=a["source"],
                )
                self.db.add(new_asset)
                await self.db.flush()  # get ID
                asset_id_map[a["value"]] = new_asset.id

                # add history
                self.db.add(AssetHistory(asset_id=new_asset.id, event="Discovered"))
            else:
                asset_id_map[a["value"]] = existing.id
                self.db.add(
                    AssetHistory(
                        asset_id=existing.id, event=f"Seen again via {a['source']}"
                    )
                )

        # Relationships
        rels = RelationshipEngine.infer_parent_child(deduped_assets)
        for r in rels:
            p_id = asset_id_map.get(r["parent_value"])
            c_id = asset_id_map.get(r["child_value"])
            if p_id and c_id:
                # check existing
                res = await self.db.execute(
                    select(AssetRelationship).filter(
                        AssetRelationship.parent_asset_id == p_id,
                        AssetRelationship.child_asset_id == c_id,
                    )
                )
                if not res.scalars().first():
                    self.db.add(
                        AssetRelationship(
                            parent_asset_id=p_id,
                            child_asset_id=c_id,
                            relationship_type=r["relationship_type"],
                        )
                    )

        # Findings
        deduped_findings = Deduplicator.deduplicate_findings(raw_findings)
        correlated = AssetCorrelator.correlate_findings(deduped_findings)

        for f in correlated:
            # We assume finding has scan_id injected by workflow context, but for simplicity we will just store intelligence record
            # In a full flow, findings attach to scans. We will attach them to IntelligenceRecord for the asset if asset matches.
            pass

        await self.db.commit()

    async def get_assets(self) -> List[Dict[str, Any]]:
        result = await self.db.execute(select(Asset))
        return [
            {"id": a.id, "type": a.asset_type, "value": a.value, "source": a.source}
            for a in result.scalars().all()
        ]

    async def get_asset_graph(self) -> Dict[str, Any]:
        assets_res = await self.db.execute(select(Asset))
        assets = {a.id: a for a in assets_res.scalars().all()}

        rels_res = await self.db.execute(select(AssetRelationship))
        rels = rels_res.scalars().all()

        graph = {
            "nodes": [
                {"id": a.id, "value": a.value, "type": a.asset_type}
                for a in assets.values()
            ],
            "edges": [
                {
                    "source": r.parent_asset_id,
                    "target": r.child_asset_id,
                    "type": r.relationship_type,
                }
                for r in rels
            ],
        }
        return graph
