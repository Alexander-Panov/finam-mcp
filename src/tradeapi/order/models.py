from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field

from src.tradeapi.models import Symbol


class Side(str, Enum):
    """Сторона сделки"""
    BUY = "SIDE_BUY"
    SELL = "SIDE_SELL"


class OrderType(str, Enum):
    """Тип заявки"""
    UNSPECIFIED = "ORDER_TYPE_UNSPECIFIED"
    MARKET = "ORDER_TYPE_MARKET"
    LIMIT = "ORDER_TYPE_LIMIT"
    STOP = "ORDER_TYPE_STOP"
    STOP_LIMIT = "ORDER_TYPE_STOP_LIMIT"
    MULTI_LEG = "ORDER_TYPE_MULTI_LEG"


class TimeInForce(str, Enum):
    """Срок действия заявки"""
    UNSPECIFIED = "TIME_IN_FORCE_UNSPECIFIED"
    DAY = "TIME_IN_FORCE_DAY"
    GOOD_TILL_CANCEL = "TIME_IN_FORCE_GOOD_TILL_CANCEL"
    GOOD_TILL_CROSSING = "TIME_IN_FORCE_GOOD_TILL_CROSSING"
    EXT = "TIME_IN_FORCE_EXT"
    ON_OPEN = "TIME_IN_FORCE_ON_OPEN"
    ON_CLOSE = "TIME_IN_FORCE_ON_CLOSE"
    IOC = "TIME_IN_FORCE_IOC"
    FOK = "TIME_IN_FORCE_FOK"


class StopCondition(str, Enum):
    """Условие срабатывания стоп заявки"""
    UNSPECIFIED = "STOP_CONDITION_UNSPECIFIED"
    LAST_UP = "STOP_CONDITION_LAST_UP"
    LAST_DOWN = "STOP_CONDITION_LAST_DOWN"


class ValidBefore(str, Enum):
    """Срок действия условной заявки"""
    UNSPECIFIED = "VALID_BEFORE_UNSPECIFIED"
    END_OF_DAY = "VALID_BEFORE_END_OF_DAY"
    GOOD_TILL_CANCEL = "VALID_BEFORE_GOOD_TILL_CANCEL"
    GOOD_TILL_DATE = "VALID_BEFORE_GOOD_TILL_DATE"


class OrderStatus(str, Enum):
    """Статус заявки"""
    UNSPECIFIED = "ORDER_STATUS_UNSPECIFIED"
    NEW = "ORDER_STATUS_NEW"
    PARTIALLY_FILLED = "ORDER_STATUS_PARTIALLY_FILLED"
    FILLED = "ORDER_STATUS_FILLED"
    DONE_FOR_DAY = "ORDER_STATUS_DONE_FOR_DAY"
    CANCELED = "ORDER_STATUS_CANCELED"
    REPLACED = "ORDER_STATUS_REPLACED"
    PENDING_CANCEL = "ORDER_STATUS_PENDING_CANCEL"
    REJECTED = "ORDER_STATUS_REJECTED"
    SUSPENDED = "ORDER_STATUS_SUSPENDED"
    PENDING_NEW = "ORDER_STATUS_PENDING_NEW"
    EXPIRED = "ORDER_STATUS_EXPIRED"
    FAILED = "ORDER_STATUS_FAILED"
    FORWARDING = "ORDER_STATUS_FORWARDING"
    WAIT = "ORDER_STATUS_WAIT"
    DENIED_BY_BROKER = "ORDER_STATUS_DENIED_BY_BROKER"
    REJECTED_BY_EXCHANGE = "ORDER_STATUS_REJECTED_BY_EXCHANGE"
    WATCHING = "ORDER_STATUS_WATCHING"
    EXECUTED = "ORDER_STATUS_EXECUTED"
    DISABLED = "ORDER_STATUS_DISABLED"
    LINK_WAIT = "ORDER_STATUS_LINK_WAIT"
    SL_GUARD_TIME = "ORDER_STATUS_SL_GUARD_TIME"
    SL_EXECUTED = "ORDER_STATUS_SL_EXECUTED"
    SL_FORWARDING = "ORDER_STATUS_SL_FORWARDING"
    TP_GUARD_TIME = "ORDER_STATUS_TP_GUARD_TIME"
    TP_EXECUTED = "ORDER_STATUS_TP_EXECUTED"
    TP_CORRECTION = "ORDER_STATUS_TP_CORRECTION"
    TP_FORWARDING = "ORDER_STATUS_TP_FORWARDING"
    TP_CORR_GUARD_TIME = "ORDER_STATUS_TP_CORR_GUARD_TIME"


class Leg(BaseModel):
    """Лег для мульти лег заявки"""
    symbol: Symbol
    quantity: Decimal = Field(..., description="Количество")
    side: Side = Field(..., description="Сторона")


class Order(BaseModel):
    """Информация о заявке"""
    symbol: Symbol
    quantity: Decimal = Field(description="Количество в шт.")
    side: Side = Field(description="Сторона (long или short)")
    type: OrderType = Field(description="Тип заявки")
    time_in_force: TimeInForce = Field(TimeInForce.UNSPECIFIED, description="Срок действия заявки")
    limit_price: Decimal | None = Field(None, description="Необходимо для лимитной и стоп лимитной заявки")
    stop_price: Decimal | None = Field(None, description="Необходимо для стоп рыночной и стоп лимитной заявки")
    stop_condition: StopCondition = Field(StopCondition.UNSPECIFIED, description="Необходимо для стоп рыночной и стоп лимитной заявки")
    legs: list[Leg] | None = Field(None, description="Необходимо для мульти лег заявки")
    client_order_id: str | None = Field(None, max_length=20, description="Уникальный идентификатор заявки")
    valid_before: ValidBefore | None = Field(None, description="Срок действия условной заявки")
    comment: str | None = Field(None, max_length=128, description="Метка заявки")


class OrderState(BaseModel):
    """Состояние заявки"""
    order_id: str = Field(..., description="Идентификатор заявки")
    exec_id: str | None = Field(None, description="Идентификатор исполнения")
    status: OrderStatus = Field(..., description="Статус заявки")
    order: Order = Field(..., description="Заявка")
    transact_at: datetime | None = Field(None, description="Дата и время выставления заявки")
    accept_at: datetime | None = Field(None, description="Дата и время принятия заявки")
    withdraw_at: datetime | None = Field(None, description="Дата и время отмены заявки")


class OrdersResponse(BaseModel):
    """Список торговых заявок"""
    orders: list[OrderState] = Field(..., description="Заявки")

