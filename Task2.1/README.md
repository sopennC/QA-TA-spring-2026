# Задание 2.1 — API-тесты микросервиса объявлений

Тестовое задание Avito QA Internship (весенняя волна 2026).
Автотесты для REST API [qa-internship.avito.com](https://qa-internship.avito.com), трёхслойная архитектура: clients / managers / tests.

## Стек

- Python 3.12+
- pytest
- requests
- pydantic + pydantic-settings
- allure-pytest
- ruff

## Структура

```
avito-TA-spring/
├── clients/
│   ├── builder.py          # фабрика: создаёт HTTPClient с нужными заголовками
│   ├── http_client.py      # базовый HTTP-клиент (GET / POST, allure-вложения)
│   └── items_client.py     # методы API: create / get by id / by seller / statistic
├── managers/
│   └── items_manager.py    # бизнес-логика: парсинг ответов, хелперы extract_created_id / default_stats
├── models/
│   └── items.py            # Pydantic v2 модели запросов и ответов
├── tests/
│   ├── scenarios/
│   │   └── test_items.py   # все тест-сценарии (positive / negative / corner cases)
│   └── conftest.py         # регистрация фикстур через pytest_plugins
├── utils/
│   ├── assertions/
│   │   └── items.py        # хелперы assert_create_success, assert_error_400 и др.
│   ├── constants/
│   │   └── routes.py       # enum APIRoutes с путями эндпоинтов
│   ├── fixtures/
│   │   └── items.py        # pytest-фикстуры items_client и items_manager
│   ├── fakers.py           # генераторы тестовых данных на базе Faker
│   └── logger.py           # настройка логирования
├── .env                    # базовые переменные окружения (BASE_URL)
├── .gitignore
├── BUGS.md                 # задокументированные баги сервера (BUG-1 - BUG-6)
├── TESTCASES.md            # таблица тест-кейсов с маппингом на автотесты
├── pytest.ini              # конфигурация pytest (pythonpath, allure-results)
├── requirements.txt
├── ruff.toml               # конфигурация линтера и форматтера
└── settings.py             # pydantic-settings: чтение .env / .env.override
```

## Переменные окружения

```env
BASE_URL=https://qa-internship.avito.com
```

Для локального оверрайда создай `.env.override`.

## Запуск

**macOS**
```bash
git clone https://github.com/sopennC/QA-TA-spring-2026.git
cd QA-TA-spring-2026/Task2.1
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

**Windows**
```bash
git clone https://github.com/sopennC/QA-TA-spring-2026.git
cd QA-TA-spring-2026/Task2.1
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest
```

> Два теста упадут намеренно — они фиксируют баги сервера (BUG-1, BUG-2).

## Allure-отчёт

```bash
allure serve allure-results
```

Установка Allure CLI:

**macOS** — [brew.sh](https://brew.sh)
```bash
brew install allure
```

**Windows** — [scoop.sh](https://scoop.sh)
```bash
scoop install allure
```

## Линтер и форматтер

Конфигурация: `ruff.toml`

```bash
ruff check .
ruff format .
```

## Покрытие

**Создание объявления (`POST /api/1/item`)**
- Создание с валидными данными
- Граничные значения `price`, `name`, `sellerID`
- Спецсимволы в `name`
- Идемпотентность: два одинаковых запроса создают разные объявления
- Отсутствие обязательных полей (`name`, `price`, `sellerID`)
- Нулевая и отрицательная цена (фиксируют BUG-1 и BUG-2)

**Получение объявления (`GET /api/1/item/:id`)**
- Получение по существующему ID
- Несуществующий ID: 404

**Список объявлений продавца (`GET /api/1/:sellerID/item`)**
- Продавец с объявлениями — оба UUID присутствуют в ответе
- Продавец без объявлений: пустой массив

**Статистика (`GET /api/1/statistic/:id`)**
- Получение по существующему ID
- Несуществующий ID: 404

**Flow**
- Создание, получение по ID, получение статистики
