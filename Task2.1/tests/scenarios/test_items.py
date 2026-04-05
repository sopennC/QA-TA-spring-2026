import uuid

import allure
import pytest

from managers.items_manager import ItemsManager, default_stats, extract_created_id
from models.items import CreateItemRequest
from utils.assertions.items import (
    assert_create_success,
    assert_error_400,
    assert_item_fields,
    assert_not_found,
    assert_stats_valid,
)
from utils.fakers import random_item_name, random_price, random_seller_id


@allure.feature("Create Item")
class TestCreateItem:

    @allure.title("Create item with valid data")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_item_positive(self, items_manager: ItemsManager):
        name = random_item_name("TestItem")
        price = random_price()
        seller_id = random_seller_id()

        with allure.step("POST item"):
            response = items_manager.client.create_item_api(
                CreateItemRequest(name=name, price=price, seller_id=seller_id, statistics=default_stats())
            )

        with allure.step("check status and UUID"):
            created = assert_create_success(response)
            item_id = extract_created_id(created.status)

        with allure.step("GET item by ID — check fields"):
            items = items_manager.get_item_by_id(item_id)
            assert len(items) == 1
            assert_item_fields(items[0], name, price, seller_id)


@allure.feature("Get Item")
class TestGetItemByID:

    @allure.title("Get existing item by ID")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_item_by_id_positive(self, items_manager: ItemsManager):
        name = random_item_name("TestGet")
        price = random_price()
        seller_id = random_seller_id()

        with allure.step("POST item"):
            created = items_manager.create_item(name, price, seller_id)
            item_id = extract_created_id(created.status)

        with allure.step("GET item by ID"):
            items = items_manager.get_item_by_id(item_id)

        with allure.step("check fields"):
            assert len(items) == 1
            assert_item_fields(items[0], name, price, seller_id)
            assert items[0].id == item_id


@allure.feature("Get Items by Seller")
class TestGetItemsBySellerID:

    @allure.title("Get all items by seller ID")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_items_by_seller_id_positive(self, items_manager: ItemsManager):
        seller_id = random_seller_id()
        name1 = random_item_name("Item1")
        name2 = random_item_name("Item2")
        price = random_price()

        with allure.step("POST item 1"):
            r1 = items_manager.create_item(name1, price, seller_id)
            id1 = extract_created_id(r1.status)

        with allure.step("POST item 2"):
            r2 = items_manager.create_item(name2, price, seller_id)
            id2 = extract_created_id(r2.status)

        with allure.step("GET items by sellerID"):
            items = items_manager.get_items_by_seller_id(seller_id)

        with allure.step("both items in list"):
            ids = {item.id for item in items}
            assert id1 in ids, "Item 1 not found in list"
            assert id2 in ids, "Item 2 not found in list"


@allure.feature("Statistics")
class TestGetStatistic:

    @allure.title("Get statistics for existing item")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_statistic_positive(self, items_manager: ItemsManager):
        with allure.step("POST item"):
            created = items_manager.create_item(random_item_name("StatTest"), random_price(), random_seller_id())
            item_id = extract_created_id(created.status)

        with allure.step("GET statistics"):
            stats = items_manager.get_statistic(item_id)

        with allure.step("stats >= 0"):
            assert len(stats) == 1
            assert_stats_valid(stats[0])


@allure.feature("Negative Scenarios")
class TestNegativeScenarios:

    @allure.title("Create item: name missing, expect 400")
    def test_create_item_without_name(self, items_manager: ItemsManager):
        with allure.step("POST name='' (empty)"):
            response = items_manager.client.create_item_api({
                "name": "",
                "price": random_price(),
                "sellerID": random_seller_id(),
                "statistics": {"likes": 1, "viewCount": 1, "contacts": 1},
            })
        assert_error_400(response)

    @allure.title("Create item: price=0 — BUG-1")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_item_with_zero_price(self, items_manager: ItemsManager):
        with allure.step("POST price=0 (BUG-1: server returns 400)"):
            response = items_manager.client.create_item_api({
                "name": random_item_name("ZeroPrice"),
                "price": 0,
                "sellerID": random_seller_id(),
                "statistics": {"likes": 1, "viewCount": 1, "contacts": 1},
            })
        assert_create_success(response)  # BUG-1: сервер вернёт 400

    @allure.title("Create item: price missing, expect 400")
    def test_create_item_without_price_field(self, items_manager: ItemsManager):
        with allure.step("POST without price field"):
            response = items_manager.client.create_item_api({
                "name": random_item_name(),
                "sellerID": random_seller_id(),
                "statistics": {"likes": 1, "viewCount": 1, "contacts": 1},
            })
        assert_error_400(response)

    @allure.title("Create item: sellerID=0, expect 400")
    def test_create_item_without_seller_id(self, items_manager: ItemsManager):
        with allure.step("POST sellerID=0"):
            response = items_manager.client.create_item_api({
                "name": "NoSeller",
                "price": 100,
                "sellerID": 0,
                "statistics": {"likes": 1, "viewCount": 1, "contacts": 1},
            })
        assert_error_400(response)

    @allure.title("Create item: price=-100, expect 400 — BUG-2")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_item_with_negative_price(self, items_manager: ItemsManager):
        with allure.step("POST price=-100 (BUG-2: server returns 200)"):
            response = items_manager.client.create_item_api({
                "name": "NegPrice",
                "price": -100,
                "sellerID": random_seller_id(),
                "statistics": {"likes": 1, "viewCount": 1, "contacts": 1},
            })
        assert_error_400(response)  # BUG-2: сервер вернёт 200

    @allure.title("Get item by ID: non-existent, expect 404")
    def test_get_item_by_id_not_found(self, items_manager: ItemsManager):
        with allure.step("GET non-existent UUID"):
            response = items_manager.client.get_item_by_id_api(str(uuid.uuid4()))
        assert_not_found(response)

    @allure.title("Get items: no listings, expect empty")
    def test_get_items_by_seller_id_not_found(self, items_manager: ItemsManager):
        with allure.step("GET unused sellerID"):
            response = items_manager.client.get_items_by_seller_id_api(random_seller_id())
        assert response.status_code == 200
        assert response.json() == []

    @allure.title("Get stats: non-existent item, expect 404")
    def test_get_statistic_not_found(self, items_manager: ItemsManager):
        with allure.step("GET non-existent UUID"):
            response = items_manager.client.get_statistic_api(str(uuid.uuid4()))
        assert_not_found(response)


@allure.feature("Corner Cases")
class TestCornerCases:

    @allure.title("Create item: sellerID outside recommended range")
    def test_create_item_with_seller_id_out_of_recommended_range(self, items_manager: ItemsManager):
        with allure.step("POST sellerID=100000"):
            response = items_manager.client.create_item_api(
                CreateItemRequest(name="OutRange", price=100, seller_id=100000, statistics=default_stats())
            )
        assert_create_success(response)

    @allure.title("Price boundary: {price}")
    @pytest.mark.parametrize("price", [1, 2147483647], ids=["min", "max_int32"])
    def test_create_item_with_boundary_price(self, items_manager: ItemsManager, price: int):
        assert_create_success(
            items_manager.client.create_item_api(
                CreateItemRequest(name=random_item_name("BoundaryPrice"), price=price, seller_id=random_seller_id(), statistics=default_stats())
            )
        )

    @allure.title("SellerID boundary: {seller_id}")
    @pytest.mark.parametrize("seller_id", [111111, 999999], ids=["min", "max"])
    def test_create_item_with_boundary_seller_id(self, items_manager: ItemsManager, seller_id: int):
        assert_create_success(
            items_manager.client.create_item_api(
                CreateItemRequest(name=random_item_name("BoundarySeller"), price=100, seller_id=seller_id, statistics=default_stats())
            )
        )

    @allure.title("Idempotency: same POST twice gives different IDs")
    def test_idempotent_create(self, items_manager: ItemsManager):
        name = random_item_name("Idempotent")
        price = 100
        seller_id = random_seller_id()

        with allure.step("First create"):
            id1 = extract_created_id(items_manager.create_item(name, price, seller_id).status)

        with allure.step("POST same data again"):
            id2 = extract_created_id(items_manager.create_item(name, price, seller_id).status)

        with allure.step("IDs must differ"):
            assert id1 != id2

    @allure.title("Name boundary: {name}")
    @pytest.mark.parametrize("name", ["A", "a" * 255], ids=["1_char", "255_chars"])
    def test_create_item_with_boundary_name(self, items_manager: ItemsManager, name: str):
        assert_create_success(
            items_manager.client.create_item_api(
                CreateItemRequest(name=name, price=100, seller_id=random_seller_id(), statistics=default_stats())
            )
        )

    @allure.title("Special characters in name field")
    def test_create_item_with_special_chars_name(self, items_manager: ItemsManager):
        seller_id = random_seller_id()

        with allure.step("POST name='!@#$%^&*()'"):
            created = assert_create_success(
                items_manager.client.create_item_api(
                    CreateItemRequest(name="!@#$%^&*()", price=100, seller_id=seller_id, statistics=default_stats())
                )
            )

        with allure.step("GET — name returned unchanged"):
            items = items_manager.get_item_by_id(extract_created_id(created.status))
            assert len(items) == 1
            assert items[0].name == "!@#$%^&*()"


@allure.feature("Flows")
class TestFlows:

    @allure.title("Flow: create item, get by ID, get statistics")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_flow_create_get_statistic(self, items_manager: ItemsManager):
        name = random_item_name("Flow")
        price = random_price()
        seller_id = random_seller_id()

        with allure.step("POST item"):
            created = items_manager.create_item(name, price, seller_id)
            item_id = extract_created_id(created.status)
            assert item_id

        with allure.step("GET item by ID"):
            items = items_manager.get_item_by_id(item_id)
            assert len(items) == 1
            assert_item_fields(items[0], name, price, seller_id)
            assert items[0].id == item_id

        with allure.step("GET statistics"):
            stats = items_manager.get_statistic(item_id)
            assert len(stats) == 1
            assert_stats_valid(stats[0])
