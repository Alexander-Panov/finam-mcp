"""Finam Account MCP - действия связанные с получением данных об аккаунте """

from fastmcp import FastMCP
from fastmcp.server.dependencies import get_context
from finam_trade_api.account import GetTransactionsResponse, GetTradesResponse
from pydantic import AwareDatetime

from src.tradeapi.models import GetAccountResponse

account_mcp = FastMCP(name="FinamAccountServer")


@account_mcp.tool(tags={"account"})
async def get_info() -> GetAccountResponse:
    """Получение информации по конкретному счету (статус и тип аккаунта, доступные средства, дневная прибыль, открытые позиции (количество, средняя цена, прибыль/убыток), тип портфеля)"""
    finam_client = get_context().get_state("finam_client")
    return await finam_client.get_account_info()


@account_mcp.tool(tags={"account"})
async def get_transactions(start_time: AwareDatetime, end_time: AwareDatetime, limit: int = 10) -> GetTransactionsResponse:
    """Получение списка транзакций аккаунта"""
    finam_client = get_context().get_state("finam_client")
    return await finam_client.get_transactions(start_time, end_time, limit)


@account_mcp.tool(tags={"account"})
async def get_trades(start_time: AwareDatetime, end_time: AwareDatetime, limit: int = 10) -> GetTradesResponse:
    """Получение истории по сделкам аккаунта"""
    finam_client = get_context().get_state("finam_client")
    return await finam_client.get_trades(start_time, end_time, limit)
