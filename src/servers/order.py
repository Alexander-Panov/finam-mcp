"""Finam Trade MCP - действия связанные с торговлей """
from decimal import Decimal

from fastmcp import FastMCP
from fastmcp.server.dependencies import get_context

from src.tradeapi.order.models import OrdersResponse, OrderState, Order, Side, OrderType

order_mcp = FastMCP(name="FinamOrderServer")


@order_mcp.tool(tags={"order"})
async def get_orders() -> OrdersResponse:
    """Получение списка заявок для аккаунта"""
    finam_client = get_context().get_state("finam_client")
    return await finam_client.get_orders()


@order_mcp.tool(tags={"order"})
async def get_order(order_id: str) -> OrderState:
    """Получение информации о конкретном ордере"""
    finam_client = get_context().get_state("finam_client")
    return await finam_client.get_order(order_id)


@order_mcp.tool(tags={"order"}, meta={"sensitive": True})
async def place_order(order: Order) -> OrderState:
    """Выставление биржевой заявки"""
    finam_client = get_context().get_state("finam_client")
    return await finam_client.place_order(order)


@order_mcp.tool(tags={"order"}, meta={"sensitive": True})
async def cancel_order(order_id: str) -> OrderState:
    """Отмена биржевой заявки"""
    finam_client = get_context().get_state("finam_client")
    return await finam_client.cancel_order(order_id)
