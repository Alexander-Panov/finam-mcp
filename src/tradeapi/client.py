from datetime import datetime

from finam_trade_api import Client, TokenManager, ErrorModel, FinamTradeApiError
from finam_trade_api.account import GetTransactionsRequest
from finam_trade_api.assets import AssetsResponse
from finam_trade_api.instruments import BarsRequest, TimeFrame

from src.tradeapi.models import GetTradesRequest, AssetParamsResponse
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

    """ Аккаунт """

    async def get_account_info(self):
        return await self.client.account.get_account_info(self.account_id)

    async def get_transactions(self, start_time: str, end_time: str, limit: int = 10):
        return await self.client.account.get_transactions(
            GetTransactionsRequest(account_id=self.account_id, start_time=start_time, end_time=end_time, limit=limit))

    async def get_trades(self, start_time: str, end_time: str, limit: int = 10):
        return await self.client.account.get_trades(
            GetTradesRequest(account_id=self.account_id, start_time=start_time, end_time=end_time, limit=limit))

    """ Assets """

    async def get_assets(self):
        assets_client = self.client.assets
        response, ok = await assets_client._exec_request(
            assets_client.RequestMethod.GET,
            f"{assets_client._url}"
        )

        if not ok:
            err = ErrorModel(**response)
            raise FinamTradeApiError(f"code={err.code} | message={err.message} | details={err.details}")

        return AssetsResponse(**response)

    async def get_asset(self, symbol: str):
        return await self.client.assets.get_asset(symbol, self.account_id)

    async def get_asset_params(self, symbol: str):
        assets_client = self.client.assets
        response, ok = await assets_client._exec_request(
            assets_client.RequestMethod.GET,
            f"{assets_client._url}/{symbol}/params",
            params={"account_id": self.account_id},
        )

        if not ok:
            err = ErrorModel(**response)
            raise FinamTradeApiError(f"code={err.code} | message={err.message} | details={err.details}")

        return AssetParamsResponse(**response)

    async def get_exchanges(self):
        return await self.client.assets.get_exchanges()

    async def get_options_chain(self, underlying_symbol: str):
        return await self.client.assets.get_options_chain(underlying_symbol)

    async def get_schedule(self, symbol: str):
        return await self.client.assets.get_schedule(symbol)

    """ Market Data """

    async def get_bars(self, symbol: str, start_time: datetime, end_time: datetime,
                       timeframe: TimeFrame):
        return await self.client.instruments.get_bars(
            BarsRequest(symbol=symbol, start_time=start_time.isoformat(), end_time=end_time.isoformat(), timeframe=timeframe))

    async def get_last_quote(self, symbol: str):
        return await self.client.instruments.get_last_quote(symbol)

    async def get_last_trades(self, symbol: str):
        return await self.client.instruments.get_last_trades(symbol)

    async def get_order_book(self, symbol: str):
        return await self.client.instruments.get_order_book(symbol)

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
