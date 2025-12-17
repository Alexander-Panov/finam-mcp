"""E2E tests for Middleware module."""

from unittest.mock import patch

import pytest
from fastmcp.exceptions import ToolError

from src.config import settings


@pytest.fixture
def mock_settings():
    """Fixture that provides a mock settings object with valid credentials by default."""
    with patch("src.middleware.settings") as mock:
        mock.FINAM_API_KEY = settings.FINAM_API_KEY
        mock.FINAM_ACCOUNT_ID = settings.FINAM_ACCOUNT_ID
        yield mock


@pytest.fixture
def mock_headers():
    """Fixture that provides a mock for get_http_headers."""
    with patch("src.middleware.get_http_headers") as mock:
        mock.return_value = {
            "finam-api-key": settings.FINAM_API_KEY,
            "finam-account-id": settings.FINAM_ACCOUNT_ID,
        }
        yield mock


class TestMiddlewareMissingCredentials:
    """Tests for missing credentials scenarios."""

    async def test_missing_api_key(self, mock_settings, mcp_client):
        """Test middleware fails when FINAM_API_KEY is not provided."""
        # Override settings to have missing API key
        mock_settings.FINAM_API_KEY = None

        with pytest.raises(ToolError) as exc_info:
            await mcp_client.call_tool("account_get_portfolio")

        assert "Missing required headers/env variables" in str(exc_info.value)
        assert "FINAM-API-KEY and FINAM-ACCOUNT-ID are required" in str(exc_info.value)

    async def test_missing_account_id(self, mock_settings, mcp_client):
        """Test middleware fails when FINAM_ACCOUNT_ID is not provided."""
        # Override settings to have missing account ID
        mock_settings.FINAM_ACCOUNT_ID = None

        with pytest.raises(ToolError) as exc_info:
            await mcp_client.call_tool("account_get_portfolio")

        assert "Missing required headers/env variables" in str(exc_info.value)
        assert "FINAM-API-KEY and FINAM-ACCOUNT-ID are required" in str(exc_info.value)

    async def test_missing_both_credentials(self, mock_settings, mcp_client):
        """Test middleware fails when both credentials are not provided."""
        # Override settings to have missing credentials
        mock_settings.FINAM_API_KEY = None
        mock_settings.FINAM_ACCOUNT_ID = None

        with pytest.raises(ToolError) as exc_info:
            await mcp_client.call_tool("account_get_portfolio")

        assert "Missing required headers/env variables" in str(exc_info.value)
        assert "FINAM-API-KEY and FINAM-ACCOUNT-ID are required" in str(exc_info.value)


class TestMiddlewareInvalidCredentials:
    """Tests for invalid credentials scenarios."""

    async def test_invalid_api_key(self, mock_headers, mcp_client):
        """Test middleware fails when API key is invalid."""
        # Override headers with invalid credentials
        mock_headers.return_value = {
            "finam-api-key": "invalid_key_12345",
            "finam-account-id": "test_account_123",
        }

        with pytest.raises(ToolError) as exc_info:
            await mcp_client.call_tool("account_get_portfolio")

        assert "Api token could not be verified" in str(exc_info.value)

    async def test_invalid_account_id(self, mock_headers, mcp_client):
        """Test middleware fails when account ID is invalid."""
        # Override headers with invalid account ID
        mock_headers.return_value = {
            "finam-api-key": settings.FINAM_API_KEY,
            "finam-account-id": "999999999",
        }

        with pytest.raises(ToolError) as exc_info:
            await mcp_client.call_tool("account_get_portfolio")

        assert "Account ID 999999999 not found" in str(exc_info.value)


class TestMiddlewareSuccessfulAuth:
    """Tests for successful authentication scenarios."""

    async def test_credentials_from_headers(self, mock_headers, mcp_client):
        """Test middleware successfully uses credentials from HTTP headers."""
        response = await mcp_client.call_tool("assets_get_exchanges")
        assert response.is_error is False

    async def test_credentials_from_settings(self, mock_settings, mcp_client):
        """Test middleware successfully uses credentials from settings."""
        response = await mcp_client.call_tool("assets_get_exchanges")
        assert response.is_error is False
