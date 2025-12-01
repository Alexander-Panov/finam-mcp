# Finam MCP Server

> ⚠️**Дисклеймер**: Это **неофициальный** MCP-сервер для Finam Trade API, созданный для демонстрационных и образовательных целей. Подробнее читайте в [хабр-статье](https://habr.com/ru/articles/960538/)

MCP (Model Context Protocol) сервер для интеграции с торговой платформой Finam через Trade API.

## Возможности

Сервер предоставляет доступ к следующим функциям Finam Trade API:

- **Account** - получение информации о счёте, транзакциях и сделках
- **Assets** - работа с торговыми инструментами, биржами, опционами
- **Market Data** - получение рыночных данных (свечи, котировки, стакан)
- **Orders** - создание, отмена и мониторинг торговых заявок

## Технологии

- **Python 3.12.6**
- **[FastMCP](https://github.com/jlowin/fastmcp)** - фреймворк для создания MCP-серверов
- **[FinamTradeApiPy](https://github.com/DBoyara/FinamTradeApiPy)** - Python-обёртка для Finam Trade API

### Полезные ссылки

- [Документация Finam Trade API](https://tradeapi.finam.ru/docs/about/)
- [Postman коллекция Finam API](https://www.postman.com/emil-7238890/f-api-public-workspace)

## Быстрый старт

### Установка зависимостей

```shell
# С использованием uv (рекомендуется)
uv sync

# Или pip
pip install -e .
```

### Запуск сервера

```shell
# Простой запуск через uvicorn
uvicorn src.main:finam_mcp --port 3000
```

### Тестирование с MCP Inspector

MCP Inspector позволяет интерактивно тестировать все инструменты сервера:

```shell
npx @modelcontextprotocol/inspector
```

Подключаемся к серверу используя адрес: "http://localhost:3000/mcp" и вставляя заголовки ключа Finam API и Account ID

![MCP Inspector](images/mcp_inspector.png)

![Headers](images/headers.png)

#### Установка Claude Desktop

Для интеграции с Claude Desktop добавьте конфигурацию в файл настроек:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "Finam": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "fastmcp",
        "--with",
        "finam-trade-api",
        "fastmcp",
        "run",
        "src/main.py:finam_mcp"
      ],
      "env": {
        "PYTHONPATH": "/путь/к/проекту/finam-mcp",
        "FINAM_API_KEY": "ваш-api-ключ",
        "FINAM_ACCOUNT_ID": "ваш-account-id",
        "INCLUDE_SERVERS": "market_data"
      }
    }
  }
}
```

**Параметры конфигурации:**
- `PYTHONPATH` - абсолютный путь к директории проекта
- `FINAM_API_KEY` - ваш API ключ из личного кабинета Finam
- `FINAM_ACCOUNT_ID` - ID вашего торгового счёта
- `INCLUDE_SERVERS` - список серверов через запятую: `account`, `assets`, `market_data`, `order` (необязательно, по умолчанию включены все)

После изменения конфигурации перезапустите Claude Desktop.

## Аутентификация

Сервер использует HTTP-заголовки для аутентификации:

- `finam-api-key` - API ключ из личного кабинета Finam
- `finam-account-id` - ID вашего торгового счёта

Получить API ключ и узнать ID торгового счета можно в личном кабинете Finam Trade.

## Структура проекта

```
src/
├── main.py              # Главный MCP-сервер
├── middleware.py        # Middleware для аутентификации
├── config.py            # Конфигурация
├── servers/             # Специализированные MCP-серверы
│   ├── account.py       # Операции со счётом
│   ├── assets.py        # Работа с инструментами
│   ├── market_data.py   # Рыночные данные
│   └── order.py         # Торговые операции
└── tradeapi/            # Обёртки над Finam Trade API
    ├── finam.py         # Основной клиент
    └── order/           # Модели и клиент для ордеров
```


## Важные особенности

### Формат символов инструментов

Все инструменты указываются в формате `ТИКЕР@MIC`:
- `SBER@MOEX` - Сбербанк на Московской бирже
- `GAZP@MOEX` - Газпром на Московской бирже
- По умолчанию используются биржи: `MOEX`, `SPBE`

### Формат времени

API требует даты и время в формате ISO 8601:
- `2024-01-15T10:30:00Z`
- `2024-01-15T10:30:00+03:00`

### TimeFrame для свечей

Доступные таймфреймы из `finam_trade_api.instruments.TimeFrame`:
- `M1`, `M5`, `M15`, `M30` - минуты
- `H1`, `H4` - часы
- `D1` - день
- `W1` - неделя


## Поддержка

По вопросам и предложениям создавайте [Issue](../../issues) в репозитории.