# Reporting Engine

The Reporting Engine handles the translation of the Intelligence Graph into human-readable formats.

## Supported Formats
- **JSON**: Raw structured data for API integrations or external SIEMs.
- **CSV**: Flat tabular data for Excel / Data Science analysts.
- **PDF**: Executive summaries containing charts, risk scores, and high-level aggregation.

## Architecture
The engine uses the Strategy Pattern. The main `ReportEngine` accepts data and delegates the actual file generation to format-specific builders (`PDFGenerator`, `CSVExporter`, etc.). PDFs are generated using Jinja2 templates and WeasyPrint or similar rendering libraries.
