from fastmcp import FastMCP
from finam_trade_api.assets import (
    AssetsResponse,
    AssetResponse,
    ExchangesResponse,
    AssetParamsResponse,
    ScheduleResponse,
    OptionsChainResponse,
)

from src.servers.utils import get_finam_client
from src.tradeapi.models import Symbol

assets_mcp = FastMCP(name="FinamAssetsServer")


@assets_mcp.tool(tags={"assets"})
async def get_asset(symbol: Symbol) -> AssetResponse:
    """Получение информации по конкретному инструменту (лот, шаг цены, дата экспирации фьючерса)"""
    return await get_finam_client().get_asset(symbol)


@assets_mcp.tool(tags={"assets"})
async def get_params(symbol: Symbol) -> AssetParamsResponse:
    """Получение торговых параметров по инструменту (операции лонг/шорт, гарантийное обеспечение, ставки риска)"""
    return await get_finam_client().get_asset_params(symbol)


@assets_mcp.tool(tags={"assets"})
async def get_assets() -> AssetsResponse:
    """Получение списка доступных инструментов, их описание (символы, наименование)"""
    return await get_finam_client().get_assets()


@assets_mcp.tool(tags={"assets"})
async def get_exchanges() -> ExchangesResponse:
    """Получение списка доступных бирж, включая их названия и MIC-коды"""
    return await get_finam_client().get_exchanges()


@assets_mcp.tool(tags={"assets"})
async def get_options_chain(symbol: Symbol) -> OptionsChainResponse:
    """Получение цепочки опционов для базового актива"""
    return await get_finam_client().get_options_chain(symbol)


@assets_mcp.tool(tags={"assets"})
async def get_schedule(symbol: Symbol) -> ScheduleResponse:
    """Получение расписания торгов для указанного инструмента"""
    return await get_finam_client().get_schedule(symbol)
