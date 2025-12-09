import pytest
from finam_trade_api.assets import (
    OptionsChainResponse,
    AssetsResponse,
    ExchangesResponse,
)

from conftest import TEST_STOCK_SYMBOLS


async def test_get_assets(mcp_client):
    response = await mcp_client.call_tool("assets_get_list")
    assert response.is_error is False
    assets = AssetsResponse.model_validate(response.structured_content)
    assert assets.assets


async def test_get_exchanges(mcp_client):
    response = await mcp_client.call_tool("assets_get_exchanges")
    assert response.is_error is False
    exchanges = ExchangesResponse.model_validate(response.structured_content)
    assert exchanges.exchanges


@pytest.mark.parametrize("symbol", TEST_STOCK_SYMBOLS)
async def test_get_options_chain(mcp_client, symbol):
    response = await mcp_client.call_tool(
        "assets_get_options_chain", arguments={"symbol": symbol}
    )

    assert response.is_error is False
    assert OptionsChainResponse.model_validate(response.structured_content)
