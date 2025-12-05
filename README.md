<div align="center">

# Finam MCP Server

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.13+-green.svg)](https://github.com/jlowin/fastmcp)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

MCP (Model Context Protocol) сервер для интеграции с торговой платформой Finam через Trade API.

Комплексный MCP-сервер для Finam Trade API, позволяющий осуществлять торговые операции через AI-ассистентов, таких как Claude Desktop и Cursor, используя естественный язык.

</div>

## Содержание

- [Предварительные требования](#предварительные-требования)
- [Быстрая установка](#быстрая-установка)
- [Получение API ключей](#получение-api-ключей)
- [Возможности](#возможности)
- [Примеры запросов](#примеры-запросов)
- [Доступные инструменты](#доступные-инструменты)
- [Конфигурация MCP клиентов](#конфигурация-mcp-клиентов)
- [Важные особенности](#важные-особенности)

## Предварительные требования

Для настройки и запуска Finam MCP Server вам потребуется:

- **Терминал** (macOS/Linux) | **Command Prompt или PowerShell** (Windows)
- **Python 3.12+** (Проверьте [официальное руководство по установке](https://www.python.org/downloads/) и подтвердите версию командой: `python3 --version` в терминале)
- **uv** (Установите используя [официальное руководство](https://docs.astral.sh/uv/getting-started/installation/))
  **Совет:** `uv` можно установить через менеджер пакетов (например, `Homebrew`) или напрямую используя `curl | sh`
- **Finam Trade API ключи** (бесплатный демо-счёт доступен)
- **MCP клиент** (Claude Desktop, Cursor, VS Code и т.д.)

**Примечание: Использование MCP-сервера требует установки и настройки как самого MCP-сервера, так и MCP-клиента.**

## Быстрая установка

Выберите подходящий способ установки для вашего MCP-клиента:

- **Claude Desktop** - Локальная установка: используйте `uvx` → см. [Настройка Claude Desktop](#настройка-claude-desktop)
- **Cursor** - Локальная установка: используйте `uvx` → см. [Настройка Cursor](#настройка-cursor)
- **VS Code** - Локальная установка: используйте `uvx` → см. [Настройка VS Code](#настройка-vs-code)

**Примечание: Как показать скрытые файлы**
- macOS Finder: Command + Shift + .
- Linux файловые менеджеры: Ctrl + H
- Windows File Explorer: Alt, V, H
- Терминал (macOS/Linux): `ls -a`

<details>
<summary><b>Метод 1: Быстрая установка с uvx из PyPI</b></summary>

**Примечание: Использование MCP-сервера требует установки и настройки как самого MCP-сервера, так и MCP-клиента.**

```bash
# Установка из PyPI
uvx finam-mcp-server@latest
```

**Примечание:** Если у вас ещё нет `uv`, установите его сначала и перезапустите терминал, чтобы `uv`/`uvx` стали доступны. См. официальное руководство: https://docs.astral.sh/uv/getting-started/installation/

**Затем добавьте в конфигурацию вашего MCP-клиента:**

**Расположение конфигурационных файлов:**
- **Claude Desktop**: `~/Library/Application Support/Claude/claude_desktop_config.json` (Mac) или `%APPDATA%\Claude\claude_desktop_config.json` (Windows)
- **Cursor**: `~/.cursor/mcp.json` (Mac/Linux) или `%USERPROFILE%\.cursor\mcp.json` (Windows)

```json
{
  "mcpServers": {
    "finam": {
      "command": "uvx",
      "args": ["finam-mcp-server@latest"],
      "env": {
        "FINAM_API_KEY": "ваш-api-ключ",
        "FINAM_ACCOUNT_ID": "ваш-account-id"
      }
    }
  }
}
```

</details>

<details>
<summary><b>Метод 2: Установка из исходников с помощью uv</b></summary>

Клонируйте репозиторий и перейдите в директорию:
```bash
git clone https://github.com/Alexander-Panov/finam-mcp.git
cd finam-mcp
```

Установите зависимости:
```bash
# С использованием uv (рекомендуется)
uv sync

# Или pip
pip install -e .
```

</details>

<details>
<summary><b>Структура проекта</b></summary>

После установки/клонирования и активации виртуального окружения структура директорий должна выглядеть так:
```
finam-mcp/                  ← Рабочая директория (корень проекта)
├── src/                    ← Исходный код пакета
│   ├── __init__.py
│   ├── cli.py              ← Интерфейс командной строки
│   ├── config.py           ← Управление конфигурацией
│   ├── main.py             ← Главный MCP-сервер
│   ├── middleware.py       ← Middleware для аутентификации
│   ├── servers/            ← Специализированные MCP-серверы
│   │   ├── account.py      ← Операции со счётом
│   │   ├── assets.py       ← Работа с инструментами
│   │   ├── market_data.py  ← Рыночные данные
│   │   └── order.py        ← Торговые операции
│   └── tradeapi/           ← Обёртки над Finam Trade API
│       ├── finam.py        ← Основной клиент
│       └── order/          ← Модели и клиент для ордеров
├── tests/                  ← Тесты
├── .venv/                  ← Виртуальное окружение
├── fastmcp.json            ← Конфигурация FastMCP
├── pyproject.toml          ← Конфигурация пакета
├── README.md
└── LICENSE
```

</details>

## Получение API ключей

1. Посетите [Личный кабинет Finam Trade](https://tradeapi.finam.ru/)
2. Создайте демо-счёт (или используйте реальный счёт)
3. Сгенерируйте API ключи в разделе "API"

### Полезные ссылки

- [Документация Finam Trade API](https://tradeapi.finam.ru/docs/about/)
- [Postman коллекция Finam API](https://www.postman.com/emil-7238890/f-api-public-workspace)

## Возможности

Сервер предоставляет доступ к следующим функциям Finam Trade API:

- **Управление счётом**
  - Просмотр баланса, маржи и статуса счёта
  - Информация о транзакциях и сделках

- **Работа с активами**
  - Получение информации о торговых инструментах
  - Поиск инструментов по тикеру, бирже, типу
  - Информация о биржах и расписании торгов
  - Работа с опционами

- **Рыночные данные**
  - Получение исторических свечей с гибкими таймфреймами
  - Котировки и последние сделки
  - Стакан заявок
  - Снапшоты инструментов

- **Управление ордерами**
  - Размещение рыночных, лимитных и стоп-ордеров
  - Отмена ордеров (индивидуально или массово)
  - Получение истории ордеров и активных заявок

## Примеры запросов

<details open>
<summary><b>Базовая торговля</b></summary>

1. Какой у меня текущий баланс счёта на Finam?
2. Покажи мои текущие позиции на счёте Finam.
3. Купи 10 акций Сбербанка по рыночной цене.
4. Продай 5 акций Газпрома с лимитной ценой 150 рублей.
5. Отмени все открытые ордера.
6. Покажи все мои активные заявки.

</details>

<details>
<summary><b>Рыночные данные</b></summary>

7. Покажи дневную историю цен Сбербанка за последние 5 торговых дней.
8. Какая была цена закрытия Газпрома вчера?
9. Получи последний бар для Лукойла.
10. Покажи текущую котировку для Яндекса.
11. Получи 5-минутные свечи для Сбербанка за последние 2 часа.

</details>

<details>
<summary><b>Информация об активах</b></summary>

12. Найди информацию об инструменте SBER@MOEX.
13. Покажи все доступные акции на Московской бирже.
14. Получи расписание торгов на сегодня.

</details>

## Доступные инструменты

<details open>
<summary><b>Счёт и позиции</b></summary>

* `get_account_info()` - Просмотр баланса и статуса счёта
* `get_transactions()` - История транзакций
* `get_trades()` - История сделок

</details>

<details>
<summary><b>Активы</b></summary>

* `get_assets()` - Список всех торговых инструментов с фильтрацией
* `get_asset_params()` - Параметры конкретного инструмента
* `get_exchanges()` - Список бирж
* `get_exchange_info()` - Информация о конкретной бирже
* `get_option_boards()` - Информация о площадках опционов
* `get_trade_schedule()` - Расписание торговых сессий

</details>

<details>
<summary><b>Рыночные данные</b></summary>

* `get_candles()` - Исторические свечи с различными таймфреймами
* `get_quotes()` - Текущие котировки
* `get_order_book()` - Стакан заявок
* `get_last_trades()` - Последние сделки

</details>

<details>
<summary><b>Торговля (Ордера)</b></summary>

* `get_orders()` - Получение всех или отфильтрованных ордеров
* `place_order()` - Размещение ордера (market, limit, stop)
* `cancel_order()` - Отмена конкретного ордера
* `cancel_all_orders()` - Отмена всех открытых ордеров

</details>

## Конфигурация MCP клиентов

Ниже вы найдёте пошаговые руководства для подключения Finam MCP сервера к различным MCP клиентам.

<a id="настройка-claude-desktop"></a>
<details open>
<summary><b>Настройка Claude Desktop</b></summary>

**Примечание: Предполагается, что все [предварительные требования](#предварительные-требования) установлены.**

### Метод: uvx (Рекомендуется)

**Простой и современный подход:**

1. Откройте Claude Desktop → Settings → Developer → Edit Config

2. Добавьте эту конфигурацию:
   ```json
   {
     "mcpServers": {
       "finam": {
         "type": "stdio",
         "command": "uvx",
         "args": ["finam-mcp-server@latest"],
         "env": {
           "FINAM_API_KEY": "ваш-api-ключ",
           "FINAM_ACCOUNT_ID": "ваш-account-id"
         }
       }
     }
   }
   ```

3. Перезапустите Claude Desktop и начинайте торговать!

</details>

<a id="настройка-cursor"></a>
<details>
<summary><b>Настройка Cursor</b></summary>

**Примечание: Предполагается, что все [предварительные требования](#предварительные-требования) установлены.**

Официальная документация по настройке MCP в Cursor: https://docs.cursor.com/context/mcp

## Использование JSON конфигурации

Откройте и отредактируйте `~/.cursor/mcp.json` (macOS/Linux) или `%USERPROFILE%\.cursor\mcp.json` (Windows):

```json
{
  "mcpServers": {
    "finam": {
      "type": "stdio",
      "command": "uvx",
      "args": ["finam-mcp-server@latest"],
      "env": {
        "FINAM_API_KEY": "ваш-api-ключ",
        "FINAM_ACCOUNT_ID": "ваш-account-id"
      }
    }
  }
}
```

</details>

<a id="настройка-vs-code"></a>
<details>
<summary><b>Настройка VS Code</b></summary>

VS Code поддерживает MCP серверы через режим агента GitHub Copilot.
Официальная документация: https://code.visualstudio.com/docs/copilot/chat/mcp-servers

**Примечание: Предполагается, что все [предварительные требования](#предварительные-требования) установлены.**

## 1. Включите поддержку MCP в VS Code

1. Откройте настройки VS Code (Ctrl/Cmd + ,)
2. Найдите "chat.mcp.enabled" и отметьте галочку для включения поддержки MCP
3. Найдите "github.copilot.chat.experimental.mcp" и отметьте галочку для использования файлов инструкций

## 2. Настройте MCP сервер (рекомендуется uvx)

**Рекомендация:** Используйте **конфигурацию для конкретного workspace** (`.vscode/mcp.json`) вместо общей конфигурации пользователя.

**Для настроек workspace:**

1. Создайте `.vscode/mcp.json` в корне вашего проекта
2. Добавьте конфигурацию Finam MCP сервера вручную в файл mcp.json:

    ```json
    {
      "mcp": {
        "servers": {
          "finam": {
            "type": "stdio",
            "command": "uvx",
            "args": ["finam-mcp-server@latest"],
            "env": {
              "FINAM_API_KEY": "ваш-api-ключ",
              "FINAM_ACCOUNT_ID": "ваш-account-id"
            }
          }
        }
      }
    }
    ```

</details>

## Тестирование с MCP Inspector

MCP Inspector позволяет интерактивно тестировать все инструменты сервера:

```bash
npx @modelcontextprotocol/inspector
```

Подключитесь к серверу, используя адрес: `http://localhost:3000/mcp` и добавив заголовки с ключом Finam API и Account ID.

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

## Использование FastMCP конфигурации

Проект поддерживает декларативную конфигурацию через `fastmcp.json`:

```bash
# Запуск с автоматическим обнаружением fastmcp.json
fastmcp run

# Или явное указание файла
fastmcp run fastmcp.json

# Для разработки с Inspector UI
fastmcp dev
```

## Технологии

- **Python 3.12+**
- **[FastMCP](https://github.com/jlowin/fastmcp)** - фреймворк для создания MCP-серверов
- **[FinamTradeApiPy](https://github.com/DBoyara/FinamTradeApiPy)** - Python-обёртка для Finam Trade API

## Поддержка

По вопросам и предложениям создавайте [Issue](../../issues) в репозитории.

## Отказ от ответственности

Это демонстрационный MCP-сервер для интеграции с Finam Trade API. Не является официальным решением от Finam.

Все торговые операции осуществляются на ваш страх и риск. Автор не несёт ответственности за возможные убытки при использовании данного сервера. Тщательно проверяйте все действия, предлагаемые AI-ассистентом, особенно для сложных торговых операций.

## Лицензия

MIT License - см. файл [LICENSE](LICENSE) для деталей.
