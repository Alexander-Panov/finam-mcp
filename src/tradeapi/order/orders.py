from decimal import Decimal

from finam_trade_api import TokenManager, FinamTradeApiError, ErrorModel
from finam_trade_api.base_client import BaseClient

from src.tradeapi.order.models import OrdersResponse, OrderState, Order


class OrderClient(BaseClient):
    def __init__(self, token_manager: TokenManager):
        super().__init__(token_manager)
        self._url = "/accounts/{account_id}/orders"

    async def get_orders(self, account_id: str) -> OrdersResponse:
        """Получение списка заявок для аккаунта"""
        response, ok = await self._exec_request(
            self.RequestMethod.GET,
            self._url.format(account_id=account_id),
        )

        if not ok:
            err = ErrorModel(**response)
            raise FinamTradeApiError(
                f"code={err.code} | message={err.message} | details={err.details}"
            )

        return OrdersResponse(**response)

    async def get_order(self, order_id: str, account_id: str) -> OrderState:
        """Получение информации о конкретном ордере"""
        response, ok = await self._exec_request(
            self.RequestMethod.GET,
            self._url.format(account_id=account_id) + f"/{order_id}",
        )

        if not ok:
            err = ErrorModel(**response)
            raise FinamTradeApiError(
                f"code={err.code} | message={err.message} | details={err.details}"
            )

        return OrderState(**response)

    async def place_order(self, order: Order, account_id: str) -> OrderState:
        """Выставление биржевой заявки"""
        order_body = {
            key: ({"value": str(value)} if isinstance(value, Decimal) else value)
            for key, value in order.model_dump(exclude_unset=True).items()
        }
        response, ok = await self._exec_request(
            self.RequestMethod.POST,
            self._url.format(account_id=account_id),
            payload=order_body,
        )

        if not ok:
            err = ErrorModel(**response)
            raise FinamTradeApiError(
                f"code={err.code} | message={err.message} | details={err.details}"
            )

        return OrderState(**response)

    async def cancel_order(self, order_id: str, account_id: str) -> OrderState:
        """Отмена биржевой заявки"""
        response, ok = await self._exec_request(
            self.RequestMethod.DELETE,
            self._url.format(account_id=account_id) + f"/{order_id}",
        )

        if not ok:
            err = ErrorModel(**response)
            raise FinamTradeApiError(
                f"code={err.code} | message={err.message} | details={err.details}"
            )

        return OrderState(**response)
