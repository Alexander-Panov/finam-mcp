from typing import Annotated

from finam_trade_api.account import GetTransactionsRequest, Position
from finam_trade_api.assets.model import Status
from finam_trade_api.base_client import FinamDecimal, FinamMoney
from pydantic import BaseModel, Field, AwareDatetime

Symbol: type[str] = Annotated[
    str,
    Field(
        description="Symbol in format: TICKER@MIC",
        pattern=r"^[A-Za-z0-9._-]+@[A-Z_]+$",
        examples=["YDEX@MISX", "SBER@TQBR"],
    ),
]

Timestamp: type[AwareDatetime] = Annotated[
    AwareDatetime,
    Field(
        description="Timestamp in RFC 3339 format (ISO 8601 with timezone)",
        examples=["2024-01-15T10:30:00Z", "2024-01-15T10:30:00+03:00"],
    ),
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


class GetAccountResponse(BaseModel):
    account_id: str
    type: str
    status: str
    positions: list[Position] = Field(default_factory=list)
    cash: list[FinamMoney] = Field(default_factory=list)
    open_account_date: Timestamp
    first_non_trade_date: Timestamp
    equity: FinamDecimal | None = None
    unrealized_profit: FinamDecimal | None = None
