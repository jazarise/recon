import pytest
from typer.testing import CliRunner
from reconx.cli.main import app

runner = CliRunner()

def test_cli_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "ReconX: Unified Cyber Intelligence OS" in result.stdout

def test_cli_doctor():
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0
    assert "Running ReconX environment checks" in result.stdout
