"""CLI entry point for finam-mcp server."""
import asyncio

import sys
import os

import click

from src.tradeapi.finam_client import FinamClient


@click.command()
@click.option(
    "--transport",
    type=click.Choice(["stdio", "http"]),
    default="stdio",
    help="Transport method: stdio (default) or http",
)
@click.option(
    "--host",
    default="127.0.0.1",
    help="Host to bind for http transport (default: 127.0.0.1)",
)
@click.option(
    "--port",
    type=int,
    default=3000,
    help="Port to bind for http transport (default: 3000)",
)
@click.version_option(version="0.1.0", prog_name="finam-mcp")
def main(transport: str, host: str, port: int) -> None:
    """
    Finam MCP Server - Finam Trade API integration for Model Context Protocol.

    Запускает Finam MCP сервер для интеграции с Finam Trade API.
    Креденшалы берутся из переменных окружения:
    - FINAM_API_KEY (обязательно)
    - FINAM_ACCOUNT_ID (обязательно)
    - INCLUDE_SERVERS (опционально, например: account,market_data)

    Examples:
        finam-mcp                           # Start with stdio transport
        finam-mcp --transport http          # Start HTTP server on default port
        finam-mcp --transport http --port 8000  # Custom port
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
        click.echo("Error: Required environment variables are not set:", err=True)
        for var in missing_vars:
            click.echo(f"  - {var}", err=True)
        click.echo(
            "\nPlease set the required environment variables and try again.", err=True
        )
        click.echo("Example:", err=True)
        click.echo("  export FINAM_API_KEY=your_api_key", err=True)
        click.echo("  export FINAM_ACCOUNT_ID=your_account_id", err=True)
        sys.exit(1)

    # Проверка токена
    async def verify_token():
        """Асинхронная проверка токена."""
        client = await FinamClient.create(api_key=api_key, account_id=account_id)
        details = await client.get_jwt_token_details()
        if account_id not in details.account_ids:
            raise RuntimeError(f"Account ID {account_id} not found.")

    try:
        asyncio.run(verify_token())
    except Exception as err:
        click.echo(f"Error: {err}", err=True)
        sys.exit(1)

    from src.main import finam_mcp

    # Показываем информацию о включённых серверах
    include_servers = finam_mcp.include_tags
    if include_servers:
        click.echo(
            f"Starting Finam MCP server with enabled modules: {', '.join(include_servers)}",
            err=True,
        )
    else:
        click.echo(
            "Starting Finam MCP server with all modules enabled (account, assets, market_data, order)",
            err=True,
        )

    # Показываем информацию о транспорте
    if transport == "http":
        click.echo(f"Transport: HTTP at http://{host}:{port}", err=True)
    else:
        click.echo("Transport: STDIO", err=True)

    click.echo("", err=True)  # Пустая строка для разделения

    try:
        # Запускаем сервер с выбранным транспортом
        if transport == "stdio":
            finam_mcp.run()
        else:
            finam_mcp.run(transport="http", host=host, port=port)
    except KeyboardInterrupt:
        click.echo("\nServer stopped by user", err=True)
        sys.exit(0)
    except Exception as e:
        click.echo(f"Error starting server: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
