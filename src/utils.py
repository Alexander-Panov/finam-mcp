from src.tradeapi.finam_client import FinamClient


async def create_finam_client(api_key: str, account_id: str) -> FinamClient:
    """Создать FinamClient с проверкой токена"""
    client = await FinamClient.create(api_key=api_key, account_id=account_id)
    # Проверка токена
    details = await client.get_jwt_token_details()
    if account_id not in details.account_ids:
        raise RuntimeError(f"Account ID {account_id} not found.")
    return client
