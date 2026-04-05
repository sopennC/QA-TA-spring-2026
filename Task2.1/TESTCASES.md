# Тест-кейсы: API сервиса объявлений

**Базовый URL:** `https://qa-internship.avito.com`

---

| ID | Заголовок | Предусловия | Шаги | Ожидаемый результат | Статус | Автотест |
|----|-----------|-------------|------|---------------------|--------|----------|
| TC-POS-01 | Создание объявления с валидными данными | — | 1. `POST /api/1/item` с корректными `name`, `price`, `sellerID`, `statistics`<br>2. Проверить статус и тело ответа<br>3. `GET /api/1/item/:id` — сверить поля | 200 OK; `status` содержит UUID; поля совпадают с запросом; `Content-Type: application/json` | Passed | `TestCreateItem::test_create_item_positive` |
| TC-POS-02 | Получение объявления по ID | Создано объявление, известен UUID | 1. `GET /api/1/item/:id`<br>2. Проверить `name`, `price`, `sellerId`, `id` | 200 OK; массив из 1 элемента; все поля совпадают | Passed | `TestGetItemByID::test_get_item_by_id_positive` |
| TC-POS-03 | Все объявления продавца содержат созданные | — | 1. `POST /api/1/item` × 2 с одним `sellerID`<br>2. `GET /api/1/:sellerID/item`<br>3. Оба UUID присутствуют | 200 OK; оба ID найдены в массиве | Passed | `TestGetItemsBySellerID::test_get_items_by_seller_id_positive` |
| TC-POS-04 | Получение статистики по объявлению | Создано объявление, известен UUID | 1. `GET /api/1/statistic/:id`<br>2. Проверить `viewCount`, `contacts`, `likes` | 200 OK; массив из 1 элемента; все поля >= 0 | Passed | `TestGetStatistic::test_get_statistic_positive` |
| TC-POS-05 | Flow: создание, GET по ID, GET статистики | — | 1. `POST /api/1/item`<br>2. `GET /api/1/item/:id` — сверить поля<br>3. `GET /api/1/statistic/:id` — сверить статистику | Все три запроса 200 OK; данные согласованы | Passed | `TestFlows::test_flow_create_get_statistic` |
| TC-NEG-01 | Создание с пустым `name` | — | 1. `POST /api/1/item` с `"name": ""`<br>2. Проверить статус и сообщение | 400 Bad Request; `message` не пустое | Passed | `TestNegativeScenarios::test_create_item_without_name` |
| TC-NEG-02 | Создание без поля `price` | — | 1. `POST /api/1/item` без ключа `price`<br>2. Проверить статус | 400 Bad Request | Passed | `TestNegativeScenarios::test_create_item_without_price_field` |
| TC-NEG-03 | Создание с `sellerID=0` | — | 1. `POST /api/1/item` с `"sellerID": 0`<br>2. Проверить статус | 400 Bad Request | Passed | `TestNegativeScenarios::test_create_item_without_seller_id` |
| TC-NEG-04 | Создание с `price=0` | — | 1. `POST /api/1/item` с `"price": 0`<br>2. Проверить статус | 200 OK | **Failed (BUG-1)** | `TestNegativeScenarios::test_create_item_with_zero_price` |
| TC-NEG-05 | Создание с `price=-100` | — | 1. `POST /api/1/item` с `"price": -100`<br>2. Проверить статус | 400 Bad Request — отрицательная цена недопустима | **Failed (BUG-2)** | `TestNegativeScenarios::test_create_item_with_negative_price` |
| TC-NEG-06 | GET по несуществующему ID | — | 1. `GET /api/1/item/:random-uuid`<br>2. Проверить статус | 404 Not Found | Passed | `TestNegativeScenarios::test_get_item_by_id_not_found` |
| TC-NEG-07 | Продавец без объявлений | — | 1. `GET /api/1/:unused-sellerID/item`<br>2. Проверить тело | 200 OK; пустой массив `[]` | Passed | `TestNegativeScenarios::test_get_items_by_seller_id_not_found` |
| TC-NEG-08 | GET статистики по несуществующему ID | — | 1. `GET /api/1/statistic/:random-uuid`<br>2. Проверить статус | 404 Not Found | Passed | `TestNegativeScenarios::test_get_statistic_not_found` |
| TC-COR-01 | `sellerID` вне рекомендованного диапазона | — | 1. `POST /api/1/item` с `"sellerID": 100000`<br>2. Проверить статус | 200 OK | Passed | `TestCornerCases::test_create_item_with_seller_id_out_of_recommended_range` |
| TC-COR-02 | Граничные значения `price`: 1 и INT32_MAX | — | 1. `POST` с `price=1`<br>2. `POST` с `price=2147483647` | 200 OK для обоих | Passed | `TestCornerCases::test_create_item_with_boundary_price` |
| TC-COR-03 | Граничные значения `sellerID`: 111111 и 999999 | — | 1. `POST` с `sellerID=111111`<br>2. `POST` с `sellerID=999999` | 200 OK для обоих | Passed | `TestCornerCases::test_create_item_with_boundary_seller_id` |
| TC-COR-04 | Идемпотентность: два одинаковых POST | — | 1. `POST` с фиксированными данными — UUID-1<br>2. Тот же запрос — UUID-2<br>3. Сравнить UUID | UUID-1 != UUID-2 | Passed | `TestCornerCases::test_idempotent_create` |
| TC-COR-05 | Граничные значения `name`: 1 и 255 символов | — | 1. `POST` с `name` из 1 символа<br>2. `POST` с `name` из 255 символов | 200 OK для обоих | Passed | `TestCornerCases::test_create_item_with_boundary_name` |
| TC-COR-06 | Спецсимволы в `name` | Создано объявление | 1. `POST` с `"name": "!@#$%^&*()"`<br>2. `GET` по UUID<br>3. Сверить `name` | 200 OK; `name` возвращается без изменений | Passed | `TestCornerCases::test_create_item_with_special_chars_name` |
