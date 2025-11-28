from typing import Annotated

from finam_trade_api.account import GetTransactionsRequest
from finam_trade_api.assets.model import Status
from finam_trade_api.base_client import FinamDecimal, FinamMoney
from pydantic import BaseModel, Field

Symbol: type[str]  = Annotated[
    str,
    Field(
        description="symbol в формате: SYMBOL@MIC (например, YDEX@MISX)",
        pattern=r"^[A-Z0-9]+@[A-Z]+$",  # Regex валидация
        examples=["YDEX@MISX", "SBER@TQBR"]
    )
]

class GetTradesRequest(GetTransactionsRequest):
    account_id: str
    start_time: str
    end_time: str
    limit: int

class AssetParamsResponse(BaseModel):
    symbol: Symbol
    account_id: str
    tradeable: bool
    longable: Status | None = None
    shortable: Status | None = None
    long_risk_rate: FinamDecimal | None = None
    long_collateral: FinamMoney | None = None
    short_risk_rate: FinamDecimal | None = None
    short_collateral: FinamMoney | None = None