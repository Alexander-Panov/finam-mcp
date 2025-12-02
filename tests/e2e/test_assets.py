import pytest
from finam_trade_api.assets import OptionsChainResponse

from conftest import TEST_STOCK_SYMBOLS


@pytest.mark.parametrize("symbol", TEST_STOCK_SYMBOLS)
async def test_get_options_chain(mcp_client, symbol):
    response = await mcp_client.call_tool(
        "assets_get_options_chain",
        arguments={
            "symbol": symbol
        }
    )

    assert response.is_error is False
    assert OptionsChainResponse.model_validate(response.structured_content)
