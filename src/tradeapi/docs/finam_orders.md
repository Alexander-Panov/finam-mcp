# Заявки
https://tradeapi.finam.ru/docs/guides/rest/orders_service/

### OrdersService [​](https://tradeapi.finam.ru/docs/guides/rest/orders_service/\#ordersservice "Прямая ссылка на OrdersService")

Сервис ордеров

| Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- |
| CancelOrder | [CancelOrderRequest](https://tradeapi.finam.ru/docs/guides/rest/orders_service/#cancelorderrequest) | [OrderState](https://tradeapi.finam.ru/docs/guides/rest/orders_service/#orderstate) | Отмена биржевой заявки |
| GetOrder | [GetOrderRequest](https://tradeapi.finam.ru/docs/guides/rest/orders_service/#getorderrequest) | [OrderState](https://tradeapi.finam.ru/docs/guides/rest/orders_service/#orderstate) | Получение информации о конкретном ордере |
| GetOrders | [OrdersRequest](https://tradeapi.finam.ru/docs/guides/rest/orders_service/#ordersrequest) | [OrdersResponse](https://tradeapi.finam.ru/docs/guides/rest/orders_service/#ordersresponse) | Получение списка заявок для аккаунта |
| PlaceOrder | [Order](https://tradeapi.finam.ru/docs/guides/rest/orders_service/#order) | [OrderState](https://tradeapi.finam.ru/docs/guides/rest/orders_service/#orderstate) | Выставление биржевой заявки |

### CancelOrderRequest [​](https://tradeapi.finam.ru/docs/guides/rest/orders_service/\#cancelorderrequest "Прямая ссылка на CancelOrderRequest")

Запрос отмены торговой заявки

| Field | Type | Description |
| --- | --- | --- |
| account\_id | string | Идентификатор аккаунта |
| order\_id | string | Идентификатор заявки |

### GetOrderRequest [​](https://tradeapi.finam.ru/docs/guides/rest/orders_service/\#getorderrequest "Прямая ссылка на GetOrderRequest")

Запрос на получение конкретного ордера

| Field | Type | Description |
| --- | --- | --- |
| account\_id | string | Идентификатор аккаунта |
| order\_id | string | Идентификатор заявки |

### Leg [​](https://tradeapi.finam.ru/docs/guides/rest/orders_service/\#leg "Прямая ссылка на Leg")

Лег

| Field | Type | Description |
| --- | --- | --- |
| symbol | string | Символ инструмента |
| quantity | google.type.Decimal | Количество |
| side | Side | Сторона |

### Order [​](https://tradeapi.finam.ru/docs/guides/rest/orders_service/\#order "Прямая ссылка на Order")

Информация о заявке

| Field | Type | Description |
| --- | --- | --- |
| account\_id | string | Идентификатор аккаунта |
| symbol | string | Символ инструмента |
| quantity | google.type.Decimal | Количество в шт. |
| side | Side | Сторона (long или short) |
| type | [OrderType](https://tradeapi.finam.ru/docs/guides/rest/orders_service/#ordertype) | Тип заявки |
| time\_in\_force | [TimeInForce](https://tradeapi.finam.ru/docs/guides/rest/orders_service/#timeinforce) | Срок действия заявки |
| limit\_price | google.type.Decimal | Необходимо для лимитной и стоп лимитной заявки |
| stop\_price | google.type.Decimal | Необходимо для стоп рыночной и стоп лимитной заявки |
| stop\_condition | [StopCondition](https://tradeapi.finam.ru/docs/guides/rest/orders_service/#stopcondition) | Необходимо для стоп рыночной и стоп лимитной заявки |
| legs | [Leg](https://tradeapi.finam.ru/docs/guides/rest/orders_service/#leg) (Array) | Необходимо для мульти лег заявки |
| client\_order\_id | string | Уникальный идентификатор заявки. Автоматически генерируется, если не отправлен. (максимум 20 символов) |
| valid\_before | [ValidBefore](https://tradeapi.finam.ru/docs/guides/rest/orders_service/#validbefore) | Срок действия условной заявки. Заполняется для заявок с типом ORDER\_TYPE\_STOP, ORDER\_TYPE\_STOP\_LIMIT |
| comment | string | Метка заявки. (максимум 128 символов) |

### OrdersRequest [​](https://tradeapi.finam.ru/docs/guides/rest/orders_service/\#ordersrequest "Прямая ссылка на OrdersRequest")

Запрос получения списка торговых заявок

| Field | Type | Description |
| --- | --- | --- |
| account\_id | string | Идентификатор аккаунта |

### OrdersResponse [​](https://tradeapi.finam.ru/docs/guides/rest/orders_service/\#ordersresponse "Прямая ссылка на OrdersResponse")

Список торговых заявок

| Field | Type | Description |
| --- | --- | --- |
| orders | [OrderState](https://tradeapi.finam.ru/docs/guides/rest/orders_service/#orderstate) (Array) | Заявки |

### OrderState [​](https://tradeapi.finam.ru/docs/guides/rest/orders_service/\#orderstate "Прямая ссылка на OrderState")

Состояние заявки

| Field | Type | Description |
| --- | --- | --- |
| order\_id | string | Идентификатор заявки |
| exec\_id | string | Идентификатор исполнения |
| status | [OrderStatus](https://tradeapi.finam.ru/docs/guides/rest/orders_service/#orderstatus) | Статус заявки |
| order | [Order](https://tradeapi.finam.ru/docs/guides/rest/orders_service/#order) | Заявка |
| transact\_at | google.protobuf.Timestamp | Дата и время выставления заявки |
| accept\_at | google.protobuf.Timestamp | Дата и время принятия заявки |
| withdraw\_at | google.protobuf.Timestamp | Дата и время отмены заявки |

### OrderStatus [​](https://tradeapi.finam.ru/docs/guides/rest/orders_service/\#orderstatus "Прямая ссылка на OrderStatus")

Статус заявки

| Name | Number | Description |
| --- | --- | --- |
| ORDER\_STATUS\_UNSPECIFIED | 0 | Неопределенное значение |
| ORDER\_STATUS\_NEW | 1 | Новая заявка |
| ORDER\_STATUS\_PARTIALLY\_FILLED | 2 | Частично исполненная |
| ORDER\_STATUS\_FILLED | 3 | Исполненная |
| ORDER\_STATUS\_DONE\_FOR\_DAY | 4 | Действует в течение дня |
| ORDER\_STATUS\_CANCELED | 5 | Отменена |
| ORDER\_STATUS\_REPLACED | 6 | Заменена на другую |
| ORDER\_STATUS\_PENDING\_CANCEL | 7 | Ожидает отмены |
| ORDER\_STATUS\_REJECTED | 9 | Отклонена |
| ORDER\_STATUS\_SUSPENDED | 10 | Приостановлена |
| ORDER\_STATUS\_PENDING\_NEW | 11 | В ожидании новой |
| ORDER\_STATUS\_EXPIRED | 13 | Истекла |
| ORDER\_STATUS\_FAILED | 16 | Ошибка |
| ORDER\_STATUS\_FORWARDING | 17 | Пересылка |
| ORDER\_STATUS\_WAIT | 18 | Ожидает |
| ORDER\_STATUS\_DENIED\_BY\_BROKER | 19 | Отклонено брокером |
| ORDER\_STATUS\_REJECTED\_BY\_EXCHANGE | 20 | Отклонено биржей |
| ORDER\_STATUS\_WATCHING | 21 | Наблюдение |
| ORDER\_STATUS\_EXECUTED | 22 | Исполнена |
| ORDER\_STATUS\_DISABLED | 23 | Отключена |
| ORDER\_STATUS\_LINK\_WAIT | 24 | Ожидание ссылки |
| ORDER\_STATUS\_SL\_GUARD\_TIME | 27 | Защитное время SL |
| ORDER\_STATUS\_SL\_EXECUTED | 28 | Исполнена по SL |
| ORDER\_STATUS\_SL\_FORWARDING | 29 | Пересылка SL |
| ORDER\_STATUS\_TP\_GUARD\_TIME | 30 | Защитное время TP |
| ORDER\_STATUS\_TP\_EXECUTED | 31 | Исполнена по TP |
| ORDER\_STATUS\_TP\_CORRECTION | 32 | Коррекция TP |
| ORDER\_STATUS\_TP\_FORWARDING | 33 | Пересылка TP |
| ORDER\_STATUS\_TP\_CORR\_GUARD\_TIME | 34 | Коррекция TP в защитное время |

### OrderType [​](https://tradeapi.finam.ru/docs/guides/rest/orders_service/\#ordertype "Прямая ссылка на OrderType")

Тип заявки

| Name | Number | Description |
| --- | --- | --- |
| ORDER\_TYPE\_UNSPECIFIED | 0 | Значение не указано |
| ORDER\_TYPE\_MARKET | 1 | Рыночная |
| ORDER\_TYPE\_LIMIT | 2 | Лимитная |
| ORDER\_TYPE\_STOP | 3 | Стоп заявка рыночная |
| ORDER\_TYPE\_STOP\_LIMIT | 4 | Стоп заявка лимитная |
| ORDER\_TYPE\_MULTI\_LEG | 5 | Мульти лег заявка |

### StopCondition [​](https://tradeapi.finam.ru/docs/guides/rest/orders_service/\#stopcondition "Прямая ссылка на StopCondition")

Условие срабатывания стоп заявки

| Name | Number | Description |
| --- | --- | --- |
| STOP\_CONDITION\_UNSPECIFIED | 0 | Значение не указано |
| STOP\_CONDITION\_LAST\_UP | 1 | Цена срабатывания больше текущей цены |
| STOP\_CONDITION\_LAST\_DOWN | 2 | Цена срабатывания меньше текущей цены |

### TimeInForce [​](https://tradeapi.finam.ru/docs/guides/rest/orders_service/\#timeinforce "Прямая ссылка на TimeInForce")

Срок действия заявки

| Name | Number | Description |
| --- | --- | --- |
| TIME\_IN\_FORCE\_UNSPECIFIED | 0 | Значение не указано |
| TIME\_IN\_FORCE\_DAY | 1 | До конца дня |
| TIME\_IN\_FORCE\_GOOD\_TILL\_CANCEL | 2 | Действителен до отмены |
| TIME\_IN\_FORCE\_GOOD\_TILL\_CROSSING | 3 | Действителен до пересечения |
| TIME\_IN\_FORCE\_EXT | 4 | Внебиржевая торговля |
| TIME\_IN\_FORCE\_ON\_OPEN | 5 | На открытии биржи |
| TIME\_IN\_FORCE\_ON\_CLOSE | 6 | На закрытии биржи |
| TIME\_IN\_FORCE\_IOC | 7 | Исполнить немедленно или отменить |
| TIME\_IN\_FORCE\_FOK | 8 | Исполнить полностью или отменить |

### ValidBefore [​](https://tradeapi.finam.ru/docs/guides/rest/orders_service/\#validbefore "Прямая ссылка на ValidBefore")

Срок действия условной заявки

| Name | Number | Description |
| --- | --- | --- |
| VALID\_BEFORE\_UNSPECIFIED | 0 | Значение не указано |
| VALID\_BEFORE\_END\_OF\_DAY | 1 | До конца торгового дня |
| VALID\_BEFORE\_GOOD\_TILL\_CANCEL | 2 | До отмены |
| VALID\_BEFORE\_GOOD\_TILL\_DATE | 3 | До указанной даты-времени. Данный тип на текущий момент не поддерживается при выставлении заявки |
