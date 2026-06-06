import typer
from cli import scan, workflow, report, project, doctor, dashboard

app = typer.Typer(help="ReconX Unified Command Line Interface")

app.add_typer(scan.app, name="scan", help="Manage and launch scans")
app.add_typer(workflow.app, name="workflow", help="Manage workflows")
app.add_typer(report.app, name="report", help="Generate reports")
app.add_typer(project.app, name="projects", help="Manage projects")
app.add_typer(doctor.app, name="doctor", help="Check system health")
app.add_typer(dashboard.app, name="dashboard", help="Manage the web dashboard")

if __name__ == "__main__":
    app()
