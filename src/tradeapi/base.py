from enum import Enum
from typing import Any

import httpx
from finam_trade_api import TokenManager


class RequestMethod(str, Enum):
    """
    Перечисление методов HTTP-запросов.
    """

    POST = "post"
    PUT = "put"
    GET = "get"
    DELETE = "delete"


class HttpxClient:
    """
    Базовый клиент для выполнения HTTP-запросов с использованием токенов аутентификации.

    Атрибуты:
        _token_manager (TokenManager): Менеджер токенов для управления JWT-токеном.
        _base_url (str): Базовый URL для всех запросов.
    """

    def __init__(
        self, token_manager: TokenManager, url: str = "https://api.finam.ru/v1"
    ):
        self._token_manager = token_manager
        self._base_url = url

    @property
    def _auth_headers(self):
        return (
            {"Authorization": self._token_manager.jwt_token}
            if self._token_manager.jwt_token
            else None
        )

    async def _exec_request(
        self, method: str, url: str, payload=None, **kwargs
    ) -> tuple[Any, bool]:
        uri = f"{self._base_url}{url}"

        async with httpx.AsyncClient(
            http2=True, timeout=20, headers=self._auth_headers
        ) as client:
            response = await client.request(method, uri, json=payload, **kwargs)

            if response.status_code != 200:
                if "application/json" not in response.headers.get("content-type", ""):
                    response.raise_for_status()
                return response.json(), False
            return response.json(), True
