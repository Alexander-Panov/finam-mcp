"""Finam Market MCP - действия связанные с получением рыночных данных """
from typing import Annotated

from fastmcp import FastMCP
from fastmcp.server.dependencies import get_context
from finam_trade_api.instruments import BarsResponse, QuoteResponse, OrderBookResponse, TimeFrame, TradesResponse

market_data_mcp = FastMCP(name="FinamMarketDataServer")


@market_data_mcp.tool(tags={"market_data"})
async def get_bars(symbol: Annotated[str, "Символ инструмента (ТИКЕР@MIC)"], start_time: str, end_time: str,
                   timeframe: TimeFrame) -> BarsResponse:
    """Получение исторических данных по инструменту (агрегированные свечи)"""
    finam_client = get_context().get_state("finam_client")
    return await finam_client.get_bars(symbol, start_time, end_time, timeframe)


@market_data_mcp.tool(tags={"market_data"})
async def get_last_quote(symbol: Annotated[str, "Символ инструмента (ТИКЕР@MIC)"]) -> QuoteResponse:
    """получение последней котировки инструмента (цена покупки/продажи, цена открытия/закрытия, цена последней сделки, дневной объем сделок, объем покупки/продажи)"""
    finam_client = get_context().get_state("finam_client")
    return await finam_client.get_last_quote(symbol)


@market_data_mcp.tool(tags={"market_data"})
async def get_last_trades(symbol: Annotated[str, "Символ инструмента (ТИКЕР@MIC)"]) -> TradesResponse:
    """Получение списка последних сделок по инструменту"""
    finam_client = get_context().get_state("finam_client")
    return await finam_client.get_last_trades(symbol)


@market_data_mcp.tool(tags={"market_data"})
async def get_order_book(symbol: Annotated[str, "Символ инструмента (ТИКЕР@MIC)"]) -> OrderBookResponse:
    """Получение текущего стакана по инструменту"""
    finam_client = get_context().get_state("finam_client")
    return await finam_client.get_order_book(symbol)
