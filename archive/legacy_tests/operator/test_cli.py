from typer.testing import CliRunner
from cli.main import app

runner = CliRunner()

def test_cli_doctor():
    result = runner.invoke(app, ["doctor", "check"])
    assert result.exit_code == 0
    assert "All systems operational" in result.stdout

def test_cli_scan():
    result = runner.invoke(app, ["scan", "start", "example.com"])
    assert result.exit_code == 0
    assert "example.com" in result.stdout
