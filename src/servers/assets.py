from fastmcp import FastMCP
from fastmcp.server.dependencies import get_context
from finam_trade_api.assets import AssetsResponse, AssetResponse, ExchangesResponse, AssetParamsResponse, \
    ScheduleResponse, OptionsChainResponse

from tradeapi.models import Symbol

assets_mcp = FastMCP(name="FinamAssetsServer")


@assets_mcp.tool(tags={"assets"})
async def get(symbol: Symbol) -> AssetResponse:
    """Получение информации по конкретному инструменту (лот, шаг цены, дата экспирации фьючерса)"""
    finam_client = get_context().get_state("finam_client")
    return await finam_client.get_asset(symbol)


@assets_mcp.tool(tags={"assets"})
async def get_params(symbol: Symbol) -> AssetParamsResponse:
    """Получение торговых параметров по инструменту (операции лонг/шорт, гарантийное обеспечение, ставки риска)"""
    finam_client = get_context().get_state("finam_client")
    return await finam_client.get_asset_params(symbol)


@assets_mcp.tool(tags={"assets"})
async def get_list() -> AssetsResponse:
    """Получение списка доступных инструментов, их описание (символы, наименование)"""
    finam_client = get_context().get_state("finam_client")
    return await finam_client.get_assets()


@assets_mcp.tool(tags={"assets"})
async def get_exchanges() -> ExchangesResponse:
    """Получение списка доступных бирж, включая их названия и MIC-коды"""
    finam_client = get_context().get_state("finam_client")
    return await finam_client.get_exchanges()


@assets_mcp.tool(tags={"assets"})
async def get_options_chain(symbol: Symbol) -> OptionsChainResponse:
    """Получение цепочки опционов для базового актива"""
    finam_client = get_context().get_state("finam_client")
    return await finam_client.get_options_chain(symbol)


@assets_mcp.tool(tags={"assets"})
async def get_schedule(symbol: Symbol) -> ScheduleResponse:
    """Получение расписания торгов для указанного инструмента"""
    finam_client = get_context().get_state("finam_client")
    return await finam_client.get_schedule(symbol)
