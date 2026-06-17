# Reporting Security

Generated reports often contain highly sensitive vulnerability data.

## Access Control
Reports are scoped by `Project`. A user must have authorization to access the specific `Project` to generate or view its reports.

## Data Sanitization
When generating HTML or PDF reports, user-supplied data (such as finding titles or asset names) is strictly sanitized using Jinja2's auto-escaping to prevent Server-Side XSS during the rendering phase.
