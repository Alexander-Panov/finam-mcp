from datetime import datetime, timedelta, timezone
import pytest
from finam_trade_api.instruments import TimeFrame, BarsResponse, QuoteResponse, OrderBookResponse, TradesResponse
from finam_trade_api.assets import OptionsChainResponse

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
        }
    )

    assert response.is_error is False
    assert TradesResponse.model_validate(response.structured_content)


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


async def test_get_bars_invalid_symbol(mcp_client):
    """Тест обработки ошибки при неправильном symbol"""
    end_time = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    start_time = end_time - timedelta(days=7)

    response = await mcp_client.call_tool(
        "market_data_get_bars",
        arguments={
            "symbol": TEST_INVALID_SYMBOL,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "timeframe": TimeFrame.TIME_FRAME_D
        },
        raise_on_error=False
    )

    assert response.is_error is True


async def test_get_last_quote_invalid_symbol(mcp_client):
    """Тест обработки ошибки при неправильном symbol"""
    response = await mcp_client.call_tool(
        "market_data_get_last_quote",
        arguments={
            "symbol": TEST_INVALID_SYMBOL
        },
        raise_on_error=False
    )

    assert response.is_error is True


async def test_get_last_trades_invalid_symbol(mcp_client):
    """Тест обработки ошибки при неправильном symbol"""
    response = await mcp_client.call_tool(
        "market_data_get_last_trades",
        arguments={
            "symbol": TEST_INVALID_SYMBOL
        },
        raise_on_error=False
    )

    assert response.is_error is True


async def test_get_order_book_invalid_symbol(mcp_client):
    """Тест обработки ошибки при неправильном symbol"""
    response = await mcp_client.call_tool(
        "market_data_get_order_book",
        arguments={
            "symbol": TEST_INVALID_SYMBOL
        },
        raise_on_error=False
    )

    assert response.is_error is True
