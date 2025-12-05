from fastmcp.server.dependencies import get_context

from src.tradeapi.finam_client import FinamClient


def get_finam_client() -> FinamClient:
    return get_context().get_state("finam_client")
