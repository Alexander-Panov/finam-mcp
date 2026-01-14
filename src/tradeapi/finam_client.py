from datetime import datetime

from finam_trade_api import Client, ErrorModel
from finam_trade_api.access import TokenDetailsResponse
from finam_trade_api.account import GetTransactionsRequest
from finam_trade_api.assets import AssetsResponse
from finam_trade_api.instruments import (
    TimeFrame,
    TradesResponse,
    OrderBookResponse,
    QuoteResponse,
    BarsResponse,
)
from mcp.server.auth.middleware.client_auth import AuthenticationError
from mcp.server.fastmcp.exceptions import ToolError

from src.tradeapi.base import HttpxClient, RequestMethod, TokenManager
from src.tradeapi.models import (
    GetTradesRequest,
    AssetParamsResponse,
    GetAccountResponse,
)
from src.tradeapi.order.orders import OrderClient


class FinamClient:
    def __init__(self, api_key, account_id):
        self.token_manager = TokenManager(api_key)
        self.client = Client(self.token_manager)
        self.client.orders = OrderClient(self.token_manager)  # доделка
        self.httpx_client = HttpxClient(self.token_manager)  # доделка
        self.account_id = account_id

    @classmethod
    async def create(cls, api_key, account_id):
        instance = cls(api_key, account_id)
        response, ok = await instance.httpx_client._exec_request(
            RequestMethod.POST,
            "/sessions",
            payload={"secret": instance.token_manager.token},
        )
        if not ok:
            raise AuthenticationError(response["message"])
        instance.token_manager.set_jwt_token(response["token"])
        return instance

    """ Helper """

    async def _exec_request(self, method: RequestMethod, url: str, **kwargs) -> dict:
        response, ok = await self.httpx_client._exec_request(method, url, **kwargs)

        if not ok:
            err = ErrorModel(**response)
            raise ToolError(
                f"code={err.code} | message={err.message} | details={err.details}"
            )
        return response

    """ Токен """

    async def get_jwt_token_details(self) -> TokenDetailsResponse:
        """
        Получает детали текущего JWT-токена.
        """
        return TokenDetailsResponse(
            **await self._exec_request(
                RequestMethod.POST,
                "/sessions/details",
                payload={"token": self.token_manager.jwt_token},
            )
        )

    """ Аккаунт """

    async def get_account_info(self):
        account_client = self.client.account
        return GetAccountResponse(
            **await self._exec_request(
                RequestMethod.GET, f"{account_client._url}/{self.account_id}"
            )
        )

    async def get_transactions(
        self, start_time: datetime, end_time: datetime, limit: int = 10
    ):
        return await self.client.account.get_transactions(
            GetTransactionsRequest(
                account_id=self.account_id,
                start_time=start_time.isoformat(),
                end_time=end_time.isoformat(),
                limit=limit,
            )
        )

    async def get_trades(
        self, start_time: datetime, end_time: datetime, limit: int = 10
    ):
        return await self.client.account.get_trades(
            GetTradesRequest(
                account_id=self.account_id,
                start_time=start_time.isoformat(),
                end_time=end_time.isoformat(),
                limit=limit,
            )
        )

    """ Assets """

    async def get_assets(self):
        return AssetsResponse(**await self._exec_request(RequestMethod.GET, "/assets"))

    async def get_asset(self, symbol: str):
        return await self.client.assets.get_asset(symbol, self.account_id)

    async def get_asset_params(self, symbol: str):
        return AssetParamsResponse(
            **await self._exec_request(
                RequestMethod.GET,
                f"/assets/{symbol}/params",
                params={"account_id": self.account_id},
            )
        )

    async def get_exchanges(self):
        return await self.client.assets.get_exchanges()

    async def get_options_chain(self, underlying_symbol: str):
        return await self.client.assets.get_options_chain(underlying_symbol)

    async def get_schedule(self, symbol: str):
        return await self.client.assets.get_schedule(symbol)

    """ Market Data """

    async def get_bars(
        self,
        symbol: str,
        start_time: datetime,
        end_time: datetime,
        timeframe: TimeFrame,
    ):
        return BarsResponse(
            **await self._exec_request(
                RequestMethod.GET,
                f"/instruments/{symbol}/bars",
                params={
                    "timeframe": timeframe.value,
                    "interval.start_time": start_time.isoformat(),
                    "interval.end_time": end_time.isoformat(),
                },
            )
        )

    async def get_last_quote(self, symbol: str):
        return QuoteResponse(
            **await self._exec_request(
                RequestMethod.GET,
                f"/instruments/{symbol}/quotes/latest",
            )
        )

    async def get_last_trades(self, symbol: str):
        return TradesResponse(
            **await self._exec_request(
                RequestMethod.GET,
                f"/instruments/{symbol}/trades/latest",
            )
        )

    async def get_order_book(self, symbol: str):
        return OrderBookResponse(
            **await self._exec_request(
                RequestMethod.GET,
                f"/instruments/{symbol}/orderbook",
            )
        )

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
