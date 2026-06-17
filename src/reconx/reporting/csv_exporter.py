import csv
from typing import Dict, Any, List


class CSVExporter:
    @staticmethod
    def export_assets(assets: List[Dict[str, Any]], output_path: str) -> str:
        if ".." in output_path or "\x00" in output_path:
            raise ValueError("Unsafe output path")

        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Type", "Value", "Source"])
            for a in assets:
                writer.writerow(
                    [a.get("id"), a.get("type"), a.get("value"), a.get("source")]
                )
        return output_path
