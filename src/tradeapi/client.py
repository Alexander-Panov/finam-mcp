from datetime import datetime

from finam_trade_api import Client, TokenManager, ErrorModel
from finam_trade_api.account import GetTransactionsRequest
from finam_trade_api.assets import AssetsResponse
from finam_trade_api.base_client import BaseClient
from finam_trade_api.instruments import TimeFrame, TradesResponse, OrderBookResponse, QuoteResponse, \
    BarsResponse
from mcp.server.fastmcp.exceptions import ToolError

from src.tradeapi.models import GetTradesRequest, AssetParamsResponse, GetAccountResponse
from src.tradeapi.order.orders import OrderClient


class FinamClient:
    def __init__(self, api_key, account_id):
        token_manager = TokenManager(api_key)
        self.client = Client(token_manager)
        self.client.orders = OrderClient(token_manager)  # доделка
        self.account_id = account_id

    @classmethod
    async def create(cls, api_key, account_id):
        instance = cls(api_key, account_id)
        await instance.client.access_tokens.set_jwt_token()
        return instance

    """ Helper """

    async def _exec_request(self, client: BaseClient, method: BaseClient.RequestMethod, url: str, **kwargs) -> dict:
        response, ok = await client._exec_request(method, url, **kwargs)

        if not ok:
            err = ErrorModel(**response)
            raise ToolError(f"code={err.code} | message={err.message} | details={err.details}")
        return response

    """ Аккаунт """

    async def get_account_info(self):
        account_client = self.client.account
        return GetAccountResponse(**await self._exec_request(account_client, BaseClient.RequestMethod.GET,
                                                             f"{account_client._url}/{self.account_id}"))

    async def get_transactions(self, start_time: datetime, end_time: datetime, limit: int = 10):
        return await self.client.account.get_transactions(
            GetTransactionsRequest(account_id=self.account_id, start_time=start_time.isoformat(),
                                   end_time=end_time.isoformat(), limit=limit))

    async def get_trades(self, start_time: datetime, end_time: datetime, limit: int = 10):
        return await self.client.account.get_trades(
            GetTradesRequest(account_id=self.account_id, start_time=start_time.isoformat(),
                             end_time=end_time.isoformat(), limit=limit))

    """ Assets """

    async def get_assets(self):
        assets_client = self.client.assets
        return AssetsResponse(
            **await self._exec_request(assets_client, BaseClient.RequestMethod.GET, f"{assets_client._url}"))

    async def get_asset(self, symbol: str):
        return await self.client.assets.get_asset(symbol, self.account_id)

    async def get_asset_params(self, symbol: str):
        assets_client = self.client.assets
        return AssetParamsResponse(**await self._exec_request(assets_client, BaseClient.RequestMethod.GET,
                                                              f"{assets_client._url}/{symbol}/params",
                                                              params={"account_id": self.account_id}))

    async def get_exchanges(self):
        return await self.client.assets.get_exchanges()

    async def get_options_chain(self, underlying_symbol: str):
        return await self.client.assets.get_options_chain(underlying_symbol)

    async def get_schedule(self, symbol: str):
        return await self.client.assets.get_schedule(symbol)

    """ Market Data """

    async def get_bars(self, symbol: str, start_time: datetime, end_time: datetime,
                       timeframe: TimeFrame):
        market_client = self.client.instruments
        return BarsResponse(**await self._exec_request(market_client, BaseClient.RequestMethod.GET,
                                                        f"{market_client._url}/{symbol}/bars",
                                                        params={
                                                            "timeframe": timeframe.value,
                                                            "interval.start_time": start_time.isoformat(),
                                                            "interval.end_time": end_time.isoformat(),
                                                        }, ))

    async def get_last_quote(self, symbol: str):
        market_client = self.client.instruments
        return QuoteResponse(**await self._exec_request(market_client, BaseClient.RequestMethod.GET,
                                                        f"{market_client._url}/{symbol}/quotes/latest", ))

    async def get_last_trades(self, symbol: str):
        market_client = self.client.instruments
        return TradesResponse(**await self._exec_request(market_client, BaseClient.RequestMethod.GET,
                                                         f"{market_client._url}/{symbol}/trades/latest", ))

    async def get_order_book(self, symbol: str):
        market_client = self.client.instruments
        return OrderBookResponse(**await self._exec_request(market_client, BaseClient.RequestMethod.GET,
                                                            f"{market_client._url}/{symbol}/orderbook", ))

    """ Orders """

    async def get_orders(self):
        """Получение списка заявок для аккаунта"""
        return await self.client.orders.get_orders(self.account_id)

    async def get_order(self, order_id: str):
        """Получение информации о конкретном ордере"""
        return await self.client.orders.get_order(order_id, self.account_id)

    async def place_order(self, order):
        """Выставление биржевой заявки"""
        return await self.client.orders.place_order(order, self.account_id)

    async def cancel_order(self, order_id: str):
        """Отмена биржевой заявки"""
        return await self.client.orders.cancel_order(order_id, self.account_id)
