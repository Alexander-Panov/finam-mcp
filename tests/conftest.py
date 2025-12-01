import pytest
from dotenv import load_dotenv
from fastmcp import Client

from src.main import finam_mcp

load_dotenv()  # чтобы работали заголовки


@pytest.fixture(scope="function")
async def mcp_client():
    """
    Создание in-memory MCP клиента для e2e тестирования
    """
    client = Client(finam_mcp)

    async with client:
        yield client


TEST_STOCK_SYMBOLS_RU = ["YDEX@MISX", "SBER@MISX"]
TEST_STOCK_SYMBOLS_US = ["AAPL@XNGS", "SPY@ARCX", "KO@XNYS"]

TEST_STOCK_SYMBOLS = TEST_STOCK_SYMBOLS_US
TEST_INVALID_SYMBOL = "INVALID@SYMBOL"
