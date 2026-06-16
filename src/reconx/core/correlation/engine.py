from reconx.core.models import AdapterResult
from .deduplicator import Deduplicator
from .asset_mapper import AssetMapper
from .rule_engine import RuleEngine
from .relationship_engine import RelationshipEngine
from .confidence import ConfidenceScorer
from .graph_builder import GraphBuilder

class CorrelationEngine:
    """The central orchestrator that transforms raw scan results into an intelligence graph."""

    def __init__(self):
        self.deduplicator = Deduplicator()
        self.asset_mapper = AssetMapper()
        self.rule_engine = RuleEngine()
        self.confidence_scorer = ConfidenceScorer()
        self.graph_builder = GraphBuilder()

    def process(self, raw_result: AdapterResult) -> dict:
        """
        Takes raw assets and findings and returns a correlated graph payload.
        """
        # 1. Deduplication
        deduplicated_assets = self.deduplicator.deduplicate(raw_result.assets)
        
        # 2. Asset Mapping (Implicit inference)
        implicit_assets = self.asset_mapper.map_implicit_assets(deduplicated_assets)
        all_assets = self.deduplicator.deduplicate(deduplicated_assets + implicit_assets)
        
        # 3. Confidence Scoring
        scored_assets = self.confidence_scorer.score(all_assets)
        
        # 4. Relationship Inference (via rules)
        inferred_relationships = self.rule_engine.infer_relationships(scored_assets)
        
        # Combine explicit relationships from the adapters with inferred ones
        rel_engine = RelationshipEngine()
        for rel in raw_result.relationships:
            rel_engine.add_relationship(rel.source_id, rel.target_id, rel.type)
        for rel in inferred_relationships:
            rel_engine.add_relationship(rel.source_id, rel.target_id, rel.type)
            
        final_relationships = rel_engine.get_all()

        # 5. Build Final Graph Payload
        graph_payload = self.graph_builder.build_graph(
            assets=scored_assets,
            relationships=final_relationships,
            findings=raw_result.findings
        )
        
        return graph_payload
