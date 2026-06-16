import os
import yaml
from typing import List, Dict, Any
from reconx.core.models import Asset, Relationship, RelationshipType

class RuleEngine:
    """Loads declarative YAML rules and infers relationships."""

    def __init__(self, rules_dir: str = "rules"):
        self.rules_dir = rules_dir
        self.rules = self._load_rules()

    def _load_rules(self) -> List[Dict[str, Any]]:
        loaded_rules = []
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        target_dir = os.path.join(base_dir, self.rules_dir)
        
        if not os.path.exists(target_dir):
            return loaded_rules

        for filename in os.listdir(target_dir):
            if filename.endswith(".yaml") or filename.endswith(".yml"):
                filepath = os.path.join(target_dir, filename)
                try:
                    with open(filepath, "r") as f:
                        data = yaml.safe_load(f)
                        if data and isinstance(data, list):
                            loaded_rules.extend(data)
                except Exception as e:
                    print(f"Error loading rule file {filename}: {e}")
        return loaded_rules

    def infer_relationships(self, assets: List[Asset]) -> List[Relationship]:
        """Applies loaded rules to the given assets to infer relationships."""
        inferred = []
        # Group assets by type for O(1) lookups
        assets_by_type = {}
        for a in assets:
            assets_by_type.setdefault(a.type.value, []).append(a)

        for rule in self.rules:
            match = rule.get("match", {})
            source_type = match.get("source")
            target_type = match.get("target")
            rel_type_str = rule.get("relationship")

            if not source_type or not target_type or not rel_type_str:
                continue

            try:
                rel_enum = RelationshipType(rel_type_str)
            except ValueError:
                continue

            sources = assets_by_type.get(source_type, [])
            targets = assets_by_type.get(target_type, [])

            # Simple exhaustive cross-check (in reality, we'd use regex/val checks)
            # For this MVP rule engine, if we have a match condition, we evaluate it.
            # E.g. if source SUBDOMAIN value is inside target URL value
            for src in sources:
                for tgt in targets:
                    # Very basic value correlation
                    if src.value in tgt.value or tgt.value in src.value:
                         inferred.append(
                             Relationship(
                                 source_id=src.id,
                                 target_id=tgt.id,
                                 type=rel_enum
                             )
                         )
        return inferred
