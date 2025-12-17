"""Finam Trade MCP - действия связанные с торговлей"""

from fastmcp import FastMCP

from src.servers.utils import get_finam_client
from src.tradeapi.order.models import OrdersResponse, OrderState, Order

order_mcp = FastMCP(name="FinamOrderServer")


@order_mcp.tool(tags={"order"})
async def get_orders() -> OrdersResponse:
    """Получение списка заявок для аккаунта"""
    return await get_finam_client().get_orders()


@order_mcp.tool(tags={"order"})
async def get_order(order_id: str) -> OrderState:
    """Получение информации о конкретном ордере"""
    return await get_finam_client().get_order(order_id)


@order_mcp.tool(tags={"order"}, meta={"sensitive": True})
async def place_order(order: Order) -> OrderState:
    """Выставление биржевой заявки"""
    return await get_finam_client().place_order(order)


@order_mcp.tool(tags={"order"}, meta={"sensitive": True})
async def cancel_order(order_id: str) -> OrderState:
    """Отмена биржевой заявки"""
    return await get_finam_client().cancel_order(order_id)
