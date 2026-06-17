from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from typing import Dict, List, Any


class PDFGenerator:
    @staticmethod
    def generate(data: Dict[str, Any], output_path: str) -> str:
        # Security validation for output_path
        if ".." in output_path or "\x00" in output_path:
            raise ValueError("Unsafe output path")

        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story: List[Any] = []

        # Title
        story.append(
            Paragraph(
                f"ReconX Executive Report: {data.get('project', 'Default')}",
                styles["Title"],
            )
        )
        story.append(Spacer(1, 12))

        # Summary
        exec_summary = data.get("executive_summary", {})
        story.append(Paragraph("Executive Summary", styles["Heading1"]))
        story.append(
            Paragraph(
                f"Total Assets: {exec_summary.get('total_assets', 0)}", styles["Normal"]
            )
        )
        story.append(
            Paragraph(
                f"Project Risk Score: {exec_summary.get('project_risk_score', 0)}",
                styles["Normal"],
            )
        )
        story.append(Spacer(1, 12))

        # Assets Table
        story.append(Paragraph("Assets", styles["Heading1"]))
        table_data = [["Type", "Value", "Source"]]
        for a in data.get("assets", [])[:50]:  # limit to 50 for pdf brevity
            table_data.append(
                [a.get("type", ""), a.get("value", ""), a.get("source", "")]
            )

        if len(table_data) > 1:
            t = Table(table_data)
            t.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ]
                )
            )
            story.append(t)

        doc.build(story)
        return output_path
