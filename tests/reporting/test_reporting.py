import pytest
from reconx.reporting.trend_analyzer import TrendAnalyzer
from reconx.reporting.pdf_generator import PDFGenerator
from reconx.reporting.html_generator import HTMLGenerator
from reconx.reporting.csv_exporter import CSVExporter
from reconx.reporting.json_exporter import JSONExporter


def test_trend_analyzer():
    current = {"assets": [1, 2], "findings": [1, 2, 3], "risk_score": 150}
    previous = {"assets": [1], "findings": [1], "risk_score": 100}

    trends = TrendAnalyzer.compare_scans(current, previous)
    assert trends["new_assets"] == 1
    assert trends["new_findings"] == 2
    assert trends["risk_change_percent"] == 50.0


def test_pdf_generation(tmp_path):
    out = tmp_path / "test.pdf"
    data = {"project": "Test", "assets": [], "executive_summary": {}}
    PDFGenerator.generate(data, str(out))
    assert out.exists()


def test_html_generation(tmp_path):
    out = tmp_path / "test.html"
    data = {
        "project": "Test",
        "assets": [],
        "executive_summary": {"recommendations": []},
    }
    gen = HTMLGenerator(templates_dir="src/reconx/templates/reports")
    gen.generate("executive", data, str(out))
    assert out.exists()


def test_csv_export(tmp_path):
    out = tmp_path / "test.csv"
    CSVExporter.export_assets([{"id": 1, "type": "Host", "value": "test"}], str(out))
    assert out.exists()


def test_json_export(tmp_path):
    out = tmp_path / "test.json"
    JSONExporter.export({"project": "Test"}, str(out))
    assert out.exists()


def test_security_validation(tmp_path):
    with pytest.raises(ValueError):
        PDFGenerator.generate({}, str(tmp_path / "../test.pdf"))
