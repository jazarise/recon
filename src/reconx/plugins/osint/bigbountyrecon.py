from reconx.core.plugin_manager.interface import ReconXPlugin
from reconx.core.schemas import Organization

class BigBountyReconPlugin(ReconXPlugin):
    name = "bigbountyrecon"
    version = "1.0.0"
    description = "Extracts information for bounty targets"

    def run(self, target: str, **kwargs):
        return {"raw_output": f"{target.split('.')[0].capitalize()}"}

    def normalize(self, results):
        return [Organization(name=results.get("raw_output", "Unknown"), domain="")]
