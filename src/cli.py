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
    - INCLUDE_SERVERS (опционально)

    Returns:
        Exit code (0 for success, 1 for error)
    """
    # Проверяем наличие обязательных переменных окружения
    api_key = os.getenv("FINAM_API_KEY")
    account_id = os.getenv("FINAM_ACCOUNT_ID")

    missing_vars = []
    if not api_key:
        missing_vars.append("FINAM_API_KEY")
    if not account_id:
        missing_vars.append("FINAM_ACCOUNT_ID")

    if missing_vars:
        print("Error: Required environment variables are not set:", file=sys.stderr)
        for var in missing_vars:
            print(f"  - {var}", file=sys.stderr)
        print("\nPlease set the required environment variables and try again.", file=sys.stderr)
        print("Example:", file=sys.stderr)
        print("  export FINAM_API_KEY=your_api_key", file=sys.stderr)
        print("  export FINAM_ACCOUNT_ID=your_account_id", file=sys.stderr)
        return 1

    from src.main import finam_mcp

    # Показываем информацию о включённых серверах
    include_servers = finam_mcp.include_tags
    if include_servers:
        print(f"Starting Finam MCP server with enabled modules: {', '.join(include_servers)}", file=sys.stderr)
    else:
        print("Starting Finam MCP server with all modules enabled (account, assets, market_data, order)", file=sys.stderr)

    print("", file=sys.stderr)  # Пустая строка для разделения

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
