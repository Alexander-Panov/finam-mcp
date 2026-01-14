from enum import Enum
from typing import Any

import httpx


class RequestMethod(str, Enum):
    """
    Перечисление методов HTTP-запросов.
    """

    POST = "post"
    PUT = "put"
    GET = "get"
    DELETE = "delete"


class TokenManager:
    """
    Класс для управления токенами, включая основной токен и JWT-токен.

    Атрибуты:
        _token (str): Основной токен, передаваемый при инициализации.
        _jwt_token (str | None): JWT-токен, который может быть установлен позже.
    """

    def __init__(self, token: str):
        """
        Инициализирует экземпляр TokenManager с основным токеном.

        Параметры:
            token (str): Основной токен, используемый для аутентификации.
        """
        self._token = token
        self._jwt_token: str | None = None

    @property
    def token(self) -> str:
        """
        Возвращает основной токен.

        Возвращает:
            str: Основной токен.
        """
        return self._token

    @property
    def jwt_token(self) -> str | None:
        """
        Возвращает текущий JWT-токен.

        Возвращает:
            str | None: JWT-токен, если он установлен, иначе None.
        """
        return self._jwt_token

    def set_jwt_token(self, jwt_token: str):
        """
        Устанавливает значение JWT-токена.

        Параметры:
            jwt_token (str): Новый JWT-токен.
        """
        self._jwt_token = jwt_token


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
