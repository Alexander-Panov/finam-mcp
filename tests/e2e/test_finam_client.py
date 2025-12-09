import pytest
from mcp.server.auth.middleware.client_auth import AuthenticationError

from config import settings
from tradeapi.finam_client import FinamClient


async def test_incorrect_jwt_token():
    with pytest.raises(AuthenticationError, match="Api token could not be verified"):
        await FinamClient.create(api_key="_" + settings.FINAM_API_KEY, account_id=settings.FINAM_ACCOUNT_ID)


async def test_get_jwt_token():
    finam_client = await FinamClient.create(api_key=settings.FINAM_API_KEY, account_id=settings.FINAM_ACCOUNT_ID)
    details = await finam_client.get_jwt_token_details()

    assert settings.FINAM_ACCOUNT_ID in details.account_ids
