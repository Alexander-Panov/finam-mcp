from fastmcp import FastMCP
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware

from src.config import settings
from src.middleware import FinamCredentialsMiddleware
from src.servers.account import account_mcp
from src.servers.assets import assets_mcp
from src.servers.market_data import market_data_mcp
from src.servers.order import order_mcp

finam_mcp = FastMCP("FinamMCP", include_tags=settings.INCLUDE_SERVERS)
finam_mcp.mount(account_mcp, prefix="account")
finam_mcp.mount(market_data_mcp, prefix="market_data")
finam_mcp.mount(assets_mcp, prefix="assets")
finam_mcp.mount(order_mcp, prefix="order")

finam_mcp.add_middleware(FinamCredentialsMiddleware())
finam_mcp.add_middleware(ErrorHandlingMiddleware())

if __name__ == "__main__":
    finam_mcp.run(transport="http", host="127.0.0.1", port=3000)
