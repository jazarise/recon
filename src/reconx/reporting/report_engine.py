from sqlalchemy.ext.asyncio import AsyncSession
from reconx.reporting.report_builder import ReportBuilder
from reconx.reporting.pdf_generator import PDFGenerator
from reconx.reporting.html_generator import HTMLGenerator
from reconx.reporting.csv_exporter import CSVExporter
from reconx.reporting.json_exporter import JSONExporter
import os


class ReportEngine:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.builder = ReportBuilder(db)

    async def export_report(self, format_type: str, output_dir: str = "reports") -> str:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        data = await self.builder.build_executive_data()

        if format_type.lower() == "pdf":
            out = os.path.join(output_dir, "report.pdf")
            return PDFGenerator.generate(data, out)
        elif format_type.lower() == "html":
            out = os.path.join(output_dir, "report.html")
            html_gen = HTMLGenerator()
            return html_gen.generate("executive", data, out)
        elif format_type.lower() == "csv":
            out = os.path.join(output_dir, "assets.csv")
            return CSVExporter.export_assets(data.get("assets", []), out)
        elif format_type.lower() == "json":
            out = os.path.join(output_dir, "report.json")
            return JSONExporter.export(data, out)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
