from fastmcp.exceptions import ToolError
from fastmcp.server.dependencies import get_http_headers
from fastmcp.server.middleware import Middleware, MiddlewareContext

from src.config import settings
from src.tradeapi.client import FinamClient


class FinamCredentialsMiddleware(Middleware):
    """Middleware для создания FinamClient из заголовков и добавления в контекст."""

    async def on_call_tool(self, context: MiddlewareContext, call_next):
        """Перехватываем все вызовы tools."""

        # Получаем заголовки из HTTP запроса
        headers = get_http_headers()

        # Извлекаем необходимые заголовки
        api_key = headers.get("finam-api-key") or settings.FINAM_API_KEY
        account_id = headers.get("finam-account-id") or settings.FINAM_ACCOUNT_ID

        # Проверяем наличие обязательных заголовков
        if not api_key or not account_id:
            raise ToolError(
                "Missing required headers/env variables: FINAM-API-KEY and FINAM-ACCOUNT-ID are required"
            )

        # Создаем клиент Finam
        finam_client = await FinamClient.create(
            api_key=api_key,
            account_id=account_id
        )

        # Сохраняем клиента в state контекста
        if context.fastmcp_context:
            context.fastmcp_context.set_state("finam_client", finam_client)

        # Продолжаем выполнение
        return await call_next(context)