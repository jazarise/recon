import typer
from reconx.cli.plugins import app as plugins_app
from reconx.cli.workflow import app as workflow_app
from reconx.cli.assets import app as assets_app
from reconx.cli.reports import app as reports_app

app = typer.Typer(help="ReconX CLI")
app.add_typer(plugins_app, name="plugins")
app.add_typer(workflow_app, name="workflow")
app.add_typer(assets_app, name="assets")
app.add_typer(reports_app, name="reports")


@app.command("dashboard")
def main_dashboard():
    from reconx.cli.reports import dashboard

    dashboard()


@app.command("findings")
def findings():
    from reconx.cli.assets import list_findings

    list_findings()


@app.command("risk")
def risk():
    from reconx.cli.assets import risk_summary

    risk_summary()


if __name__ == "__main__":
    app()
