from typer.testing import CliRunner
from reconx.cli.main import app
from reconx.cli.plugins import app as plugins_app
from reconx.cli.workflow import app as workflow_app
from reconx.cli.assets import app as assets_app
from reconx.cli.reports import app as reports_app

runner = CliRunner()


def test_main_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0


def test_plugins_help():
    result = runner.invoke(plugins_app, ["--help"])
    assert result.exit_code == 0


def test_workflow_help():
    result = runner.invoke(workflow_app, ["--help"])
    assert result.exit_code == 0


def test_assets_help():
    result = runner.invoke(assets_app, ["--help"])
    assert result.exit_code == 0


def test_reports_help():
    result = runner.invoke(reports_app, ["--help"])
    assert result.exit_code == 0
