import os
import re
from reconx.core.models import Finding

class AcquiFinderCollector:
    def __init__(self):
        self.api_key = os.getenv("Apify_API_KEY", "MOCK_API_KEY")

    def collect(self, target: str, **kwargs) -> list:
        if self.api_key == "MOCK_API_KEY":
            # For testing or if no key is provided
            return [
                Finding(
                    category="acquisition",
                    source="acquifinder",
                    value=f"{target} acquires MOCK_COMPANY",
                    metadata={"target": target, "acquired": "MOCK_COMPANY"}
                )
            ]
            
        from apify_client import ApifyClient
        client = ApifyClient(self.api_key)
        query = f'site:crunchbase.com "{target} acquires"'
        run_input = {
            "queries": query,
            "resultsPerPage": 100,
            "maxPagesPerQuery": 2,
        }
        
        try:
            run = client.actor("apify/google-search-scraper").call(run_input=run_input)
            dataset_items = client.dataset(run["defaultDatasetId"]).iterate_items()
            
            titles = [res["title"] for item in dataset_items for res in item.get("organicResults", [])]
            pattern = rf"{target} acquires ([^-]+)"
            acquisitions = re.findall(pattern, " ".join(titles), re.IGNORECASE)
            
            findings = []
            for acq in set(acquisitions):
                acq = acq.strip()
                finding = Finding(
                    category="acquisition",
                    source="acquifinder",
                    value=f"{target} acquires {acq}",
                    metadata={"target": target, "acquired": acq}
                )
                findings.append(finding)
            return findings
            
        except Exception as e:
            return [
                Finding(
                    category="error",
                    source="acquifinder",
                    value=f"Error scraping: {e}",
                    metadata={"target": target}
                )
            ]
