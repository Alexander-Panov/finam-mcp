"""Finam Market MCP - действия связанные с получением рыночных данных"""

from datetime import datetime

from fastmcp import FastMCP
from finam_trade_api.instruments import (
    BarsResponse,
    QuoteResponse,
    OrderBookResponse,
    TimeFrame,
    TradesResponse,
)
from src.servers.utils import get_finam_client
from src.tradeapi.models import Symbol

market_data_mcp = FastMCP(name="FinamMarketDataServer")


@market_data_mcp.tool(tags={"market_data"})
async def get_bars(
    symbol: Symbol, start_time: datetime, end_time: datetime, timeframe: TimeFrame
) -> BarsResponse:
    """Получение исторических данных по инструменту (агрегированные свечи)"""
    return await get_finam_client().get_bars(symbol, start_time, end_time, timeframe)


@market_data_mcp.tool(tags={"market_data"})
async def get_last_quote(symbol: Symbol) -> QuoteResponse:
    """получение последней котировки инструмента (цена покупки/продажи, цена открытия/закрытия, цена последней сделки, дневной объем сделок, объем покупки/продажи)"""
    return await get_finam_client().get_last_quote(symbol)


@market_data_mcp.tool(tags={"market_data"})
async def get_last_trades(symbol: Symbol) -> TradesResponse:
    """Получение списка последних сделок по инструменту"""
    return await get_finam_client().get_last_trades(symbol)


@market_data_mcp.tool(tags={"market_data"})
async def get_order_book(symbol: Symbol) -> OrderBookResponse:
    """Получение текущего стакана по инструменту"""
    return await get_finam_client().get_order_book(symbol)
