import tempfile
import os
import json
from reconx.reporting.json_exporter import JSONExporter
from reconx.reporting.csv_exporter import CSVExporter


def test_json_exporter():
    exporter = JSONExporter()
    data = {"project": "Test Project", "findings": []}

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        output_path = tmp.name

    try:
        exporter.export(data, output_path)
        with open(output_path, "r", encoding="utf-8") as f:
            content = json.load(f)
        assert content["project"] == "Test Project"
    finally:
        if os.path.exists(output_path):
            os.unlink(output_path)


def test_csv_exporter():
    exporter = CSVExporter()
    assets = [{"id": "1", "type": "domain", "value": "example.com", "source": "test"}]

    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        output_path = tmp.name

    try:
        exporter.export_assets(assets, output_path)
        with open(output_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "example.com" in content
        assert "domain" in content
    finally:
        if os.path.exists(output_path):
            os.unlink(output_path)
