from reconx.core.plugin_manager.interface import ReconXPlugin
from reconx.core.schemas import Username, SocialProfile, Confidence

class SocialIntelPlugin(ReconXPlugin):
    name = "social_intel"
    version = "1.0.0"
    description = "Username and social intelligence module"

    def run(self, target: str, **kwargs):
        return {"raw_output": f"github.com/{target.split('.')[0]}"}

    def normalize(self, results):
        normalized = []
        for line in results.get("raw_output", "").splitlines():
            if "github.com" in line:
                user = line.split("/")[-1]
                normalized.append(Username(value=user, source="social_intel", confidence=Confidence.HIGH))
                normalized.append(SocialProfile(
                    platform="GitHub",
                    url=line.strip(),
                    username=user,
                    confidence=Confidence.HIGH
                ))
        return normalized
