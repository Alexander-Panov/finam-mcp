from finam_trade_api.account import GetTransactionsRequest
from finam_trade_api.assets.model import Status
from finam_trade_api.base_client import FinamDecimal, FinamMoney
from pydantic import BaseModel


class GetTradesRequest(GetTransactionsRequest):
    account_id: str
    start_time: str
    end_time: str
    limit: int

class AssetParamsResponse(BaseModel):
    symbol: str
    account_id: str
    tradeable: bool
    longable: Status | None = None
    shortable: Status | None = None
    long_risk_rate: FinamDecimal | None = None
    long_collateral: FinamMoney | None = None
    short_risk_rate: FinamDecimal | None = None
    short_collateral: FinamMoney | None = None