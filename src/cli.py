"""CLI entry point for finam-mcp server."""

import sys
import os

def main() -> int:
    """
    Main CLI entry point for finam-mcp.

    Запускает Finam MCP сервер через STDIO транспорт.
    Креденшалы берутся из переменных окружения:
    - FINAM_API_KEY
    - FINAM_ACCOUNT_ID

    Returns:
        Exit code (0 for success)
    """
    # Импортируем здесь, чтобы избежать проблем с импортами до запуска
    from src.main import finam_mcp

    # Проверяем наличие необходимых переменных окружения
    if not os.getenv("FINAM_API_KEY"):
        print("Warning: FINAM_API_KEY environment variable is not set", file=sys.stderr)

    if not os.getenv("FINAM_ACCOUNT_ID"):
        print("Warning: FINAM_ACCOUNT_ID environment variable is not set", file=sys.stderr)

    try:
        # Запускаем сервер через STDIO (стандартный транспорт для MCP серверов)
        finam_mcp.run()
        return 0
    except KeyboardInterrupt:
        return 0
    except Exception as e:
        print(f"Error starting server: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
