"""E2E tests for CLI module."""
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from src.cli import main
from src.config import settings


@pytest.fixture
def cli_runner():
    """Create CLI runner for testing."""
    return CliRunner()


class TestCLIMissingEnvVars:
    """Tests for missing environment variables scenarios."""

    def test_missing_api_key(self, cli_runner):
        """Test CLI fails when FINAM_API_KEY is not set."""
        result = cli_runner.invoke(main, env={"FINAM_ACCOUNT_ID": "test_account_123"}, catch_exceptions=False)

        assert result.exit_code == 1
        assert "Error: Required environment variables are not set:" in result.output
        assert "FINAM_API_KEY" in result.output

    def test_missing_account_id(self, cli_runner):
        """Test CLI fails when FINAM_ACCOUNT_ID is not set."""
        result = cli_runner.invoke(main, env={"FINAM_API_KEY": "test_api_key"}, catch_exceptions=False)

        assert result.exit_code == 1
        assert "Error: Required environment variables are not set:" in result.output
        assert "FINAM_ACCOUNT_ID" in result.output

    def test_missing_both_env_vars(self, cli_runner):
        """Test CLI fails when both environment variables are not set."""
        result = cli_runner.invoke(main, env={}, catch_exceptions=False)

        assert result.exit_code == 1
        assert "Error: Required environment variables are not set:" in result.output
        assert "FINAM_API_KEY" in result.output
        assert "FINAM_ACCOUNT_ID" in result.output
        assert "Example:" in result.output


class TestCLIInvalidToken:
    """Tests for invalid token scenarios."""

    def test_invalid_api_key(self, cli_runner):
        """Test CLI fails when API key is invalid."""
        result = cli_runner.invoke(main, env={
            "FINAM_API_KEY": "invalid_key_12345",
            "FINAM_ACCOUNT_ID": "test_account_123"
        }, catch_exceptions=False)

        assert result.exit_code == 1
        assert "Error: Api token could not be verified" in result.output

    def test_invalid_account_id(self, cli_runner):
        """Test CLI fails when account ID is invalid (using real API key)."""
        if not settings.FINAM_API_KEY:
            pytest.skip("FINAM_API_KEY not set in settings")

        result = cli_runner.invoke(main, env={
            "FINAM_API_KEY": settings.FINAM_API_KEY,
            "FINAM_ACCOUNT_ID": "999999999"
        }, catch_exceptions=False)

        assert result.exit_code == 1
        assert "Error: Account ID 999999999 not found." in result.output


class TestCLISuccessfulLaunch:
    """Tests for successful CLI launch scenarios."""

    @pytest.fixture
    def env(self):
        return {
            "FINAM_API_KEY": settings.FINAM_API_KEY,
            "FINAM_ACCOUNT_ID": settings.FINAM_ACCOUNT_ID
        }

    @patch("src.main.finam_mcp")
    def test_successful_launch_stdio(self, mock_finam_mcp, cli_runner, env):
        """Test successful CLI launch with stdio transport."""
        if not settings.FINAM_API_KEY or not settings.FINAM_ACCOUNT_ID:
            pytest.skip("FINAM_API_KEY or FINAM_ACCOUNT_ID not set in settings")

        # Mock finam_mcp to prevent actual server start
        mock_finam_mcp.include_tags = ["account", "market_data"]
        mock_finam_mcp.run = MagicMock()

        result = cli_runner.invoke(
            main,
            ["--transport", "stdio"],
            env=env,
            catch_exceptions=False
        )

        assert result.exit_code == 0
        assert "Starting Finam MCP server" in result.output
        assert "Transport: STDIO" in result.output
        mock_finam_mcp.run.assert_called_once_with()

    @patch("src.main.finam_mcp")
    def test_successful_launch_http_default_port(self, mock_finam_mcp, cli_runner, env):
        """Test successful CLI launch with HTTP transport on default port."""
        if not settings.FINAM_API_KEY or not settings.FINAM_ACCOUNT_ID:
            pytest.skip("FINAM_API_KEY or FINAM_ACCOUNT_ID not set in settings")

        # Mock finam_mcp
        mock_finam_mcp.include_tags = []
        mock_finam_mcp.run = MagicMock()

        result = cli_runner.invoke(
            main,
            ["--transport", "http"],
            env=env,
            catch_exceptions=False
        )

        assert result.exit_code == 0
        assert "Starting Finam MCP server" in result.output
        assert "Transport: HTTP at http://127.0.0.1:3000" in result.output
        mock_finam_mcp.run.assert_called_once_with(
            transport="http",
            host="127.0.0.1",
            port=3000
        )

    @patch("src.main.finam_mcp")
    def test_successful_launch_http_custom_port(self, mock_finam_mcp, cli_runner, env):
        """Test successful CLI launch with HTTP transport on custom port."""
        if not settings.FINAM_API_KEY or not settings.FINAM_ACCOUNT_ID:
            pytest.skip("FINAM_API_KEY or FINAM_ACCOUNT_ID not set in settings")

        # Mock finam_mcp
        mock_finam_mcp.include_tags = ["order"]
        mock_finam_mcp.run = MagicMock()

        result = cli_runner.invoke(
            main,
            ["--transport", "http", "--host", "0.0.0.0", "--port", "8000"],
            env=env,
            catch_exceptions=False
        )

        assert result.exit_code == 0
        assert "Starting Finam MCP server" in result.output
        assert "Transport: HTTP at http://0.0.0.0:8000" in result.output
        mock_finam_mcp.run.assert_called_once_with(
            transport="http",
            host="0.0.0.0",
            port=8000
        )
