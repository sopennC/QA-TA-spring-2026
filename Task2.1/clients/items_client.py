import allure
from requests import Response

from clients.http_client import HTTPClient
from models.items import CreateItemRequest
from utils.constants.routes import APIRoutes


class ItemsClient:
    def __init__(self, client: HTTPClient):
        self.client = client

    @allure.step("Create item")
    def create_item_api(self, payload: CreateItemRequest | dict) -> Response:
        data = payload.model_dump(by_alias=True) if isinstance(payload, CreateItemRequest) else payload
        return self.client.post(APIRoutes.ITEM, json=data)

    @allure.step("Get item {item_id}")
    def get_item_by_id_api(self, item_id: str) -> Response:
        return self.client.get(f"{APIRoutes.ITEM}/{item_id}")

    @allure.step("Get items by seller {seller_id}")
    def get_items_by_seller_id_api(self, seller_id: int) -> Response:
        return self.client.get(f"/api/1/{seller_id}/item")

    @allure.step("Get statistic {item_id}")
    def get_statistic_api(self, item_id: str) -> Response:
        return self.client.get(f"{APIRoutes.STATISTIC}/{item_id}")
