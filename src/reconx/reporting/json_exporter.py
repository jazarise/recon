import json
from typing import Dict, Any


class JSONExporter:
    @staticmethod
    def export(data: Dict[str, Any], output_path: str) -> str:
        if ".." in output_path or "\x00" in output_path:
            raise ValueError("Unsafe output path")

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return output_path
