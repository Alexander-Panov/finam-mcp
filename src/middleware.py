from fastmcp.exceptions import ToolError
from fastmcp.server.dependencies import get_http_headers
from fastmcp.server.middleware import Middleware, MiddlewareContext

from src.config import settings
from src.utils import create_finam_client


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
        try:
            finam_client = await create_finam_client(
                api_key=api_key, account_id=account_id
            )
        except Exception as e:
            raise ToolError(str(e)) from e

        # Сохраняем клиента в state контекста
        if context.fastmcp_context:
            context.fastmcp_context.set_state("finam_client", finam_client)

        # Продолжаем выполнение
        return await call_next(context)
