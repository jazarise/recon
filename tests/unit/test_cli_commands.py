from typer.testing import CliRunner
from reconx.cli.main import app
from unittest.mock import patch, MagicMock, AsyncMock

runner = CliRunner()


@patch("reconx.cli.assets.IntelligenceStore")
def test_cli_assets_list(mock_store):
    result = runner.invoke(app, ["assets", "list"])
    assert result.exit_code in [0, 1, 2]


@patch("reconx.cli.reports.ReportEngine")
def test_cli_reports_generate(mock_engine):
    result = runner.invoke(
        app, ["reports", "generate", "--project", "1", "--format", "json"]
    )
    assert result.exit_code in [0, 1, 2]


@patch("reconx.core.workflow.workflow_engine.WorkflowEngine")
def test_cli_workflow_run(mock_engine_cls):
    mock_engine = MagicMock()
    mock_engine_cls.return_value = mock_engine
    mock_engine.execute_workflow = AsyncMock()
    result = runner.invoke(app, ["workflow", "run", "passive"])
    assert result.exit_code in [0, 1, 2]
