from datetime import datetime, timedelta, timezone
import pytest
from finam_trade_api.instruments import TimeFrame, BarsResponse, QuoteResponse, OrderBookResponse, TradesResponse

from tests.conftest import TEST_INVALID_SYMBOL, TEST_STOCK_SYMBOLS

@pytest.mark.parametrize("symbol", TEST_STOCK_SYMBOLS)
async def test_get_bars(mcp_client, symbol):
    end_time = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    start_time = end_time - timedelta(days=7)

    response = await mcp_client.call_tool(
        "market_data_get_bars",
        arguments = {
            "symbol": symbol,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "timeframe": TimeFrame.TIME_FRAME_D
        }
    )

    assert response.is_error is False
    assert BarsResponse.model_validate(response.structured_content)


@pytest.mark.parametrize("symbol", TEST_STOCK_SYMBOLS)
async def test_get_last_quote(mcp_client, symbol):
    response = await mcp_client.call_tool(
        "market_data_get_last_quote",
        arguments={
            "symbol": symbol
        }
    )

    assert response.is_error is False
    assert QuoteResponse.model_validate(response.structured_content)


@pytest.mark.parametrize("symbol", TEST_STOCK_SYMBOLS)
async def test_get_last_trades(mcp_client, symbol):
    response = await mcp_client.call_tool(
        "market_data_get_last_trades",
        arguments={
            "symbol": symbol
        },
        raise_on_error=False
    )

    if response.is_error is False:
        assert TradesResponse.model_validate(response.structured_content)
    else:
        # Trades data can be not found
        error_text = response.content[0].text
        assert "Trades not found" in error_text


@pytest.mark.parametrize("symbol", TEST_STOCK_SYMBOLS)
async def test_get_order_book(mcp_client, symbol):
    response = await mcp_client.call_tool(
        "market_data_get_order_book",
        arguments={
            "symbol": symbol
        }
    )

    assert response.is_error is False
    assert OrderBookResponse.model_validate(response.structured_content)


@pytest.mark.parametrize("tool", ["market_data_get_order_book", "market_data_get_last_trades", "market_data_get_last_quote", "market_data_get_bars"])
async def test_get_order_book_invalid_symbol(mcp_client, tool):
    """Тест обработки ошибки при неправильном symbol"""
    params = {"symbol": TEST_INVALID_SYMBOL}
    if tool == "market_data_get_bars":
        end_time = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        start_time = end_time - timedelta(days=7)

        params["timeframe"] = TimeFrame.TIME_FRAME_D
        params["start_time"] = start_time.isoformat()
        params["end_time"] = end_time.isoformat()

    response = await mcp_client.call_tool(
        tool,
        arguments=params,
        raise_on_error=False
    )

    assert response.is_error is True
    assert response.structured_content is None
    error_text = response.content[0].text
    assert "Security id doesn't exist" in error_text
