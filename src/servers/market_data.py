"""Finam Market MCP - действия связанные с получением рыночных данных """

from fastmcp import FastMCP
from fastmcp.server.dependencies import get_context
from finam_trade_api.assets import OptionsChainResponse
from finam_trade_api.instruments import BarsResponse, QuoteResponse, OrderBookResponse, TimeFrame, TradesResponse
from pydantic import AwareDatetime

from tradeapi.models import Symbol

market_data_mcp = FastMCP(name="FinamMarketDataServer")


@market_data_mcp.tool(tags={"market_data"})
async def get_bars(symbol: Symbol, start_time: AwareDatetime, end_time: AwareDatetime, timeframe: TimeFrame) -> BarsResponse:
    """Получение исторических данных по инструменту (агрегированные свечи)"""
    finam_client = get_context().get_state("finam_client")
    return await finam_client.get_bars(symbol, start_time, end_time, timeframe)


@market_data_mcp.tool(tags={"market_data"})
async def get_last_quote(symbol: Symbol) -> QuoteResponse:
    """получение последней котировки инструмента (цена покупки/продажи, цена открытия/закрытия, цена последней сделки, дневной объем сделок, объем покупки/продажи)"""
    finam_client = get_context().get_state("finam_client")
    return await finam_client.get_last_quote(symbol)


@market_data_mcp.tool(tags={"market_data"})
async def get_last_trades(symbol: Symbol) -> TradesResponse:
    """Получение списка последних сделок по инструменту"""
    finam_client = get_context().get_state("finam_client")
    return await finam_client.get_last_trades(symbol)


@market_data_mcp.tool(tags={"market_data"})
async def get_order_book(symbol: Symbol) -> OrderBookResponse:
    """Получение текущего стакана по инструменту"""
    finam_client = get_context().get_state("finam_client")
    return await finam_client.get_order_book(symbol)
