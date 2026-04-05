from clients.items_client import ItemsClient
from models.items import (
    CreateItemRequest,
    CreateItemResponse,
    ItemResponse,
    StatisticResponse,
    Statistics,
)


def extract_created_id(status: str) -> str:
    sep = " - "
    idx = status.rfind(sep)
    return status[idx + len(sep) :].strip() if idx >= 0 else ""


def default_stats() -> Statistics:
    return Statistics(likes=1, view_count=1, contacts=1)


class ItemsManager:
    def __init__(self, client: ItemsClient):
        self.client = client

    def create_item(self, name: str, price: int, seller_id: int) -> CreateItemResponse:
        payload = CreateItemRequest(name=name, price=price, seller_id=seller_id, statistics=default_stats())
        response = self.client.create_item_api(payload)
        return CreateItemResponse.model_validate(response.json())

    def get_item_by_id(self, item_id: str) -> list[ItemResponse]:
        response = self.client.get_item_by_id_api(item_id)
        return [ItemResponse.model_validate(item) for item in response.json()]

    def get_items_by_seller_id(self, seller_id: int) -> list[ItemResponse]:
        response = self.client.get_items_by_seller_id_api(seller_id)
        return [ItemResponse.model_validate(item) for item in response.json()]

    def get_statistic(self, item_id: str) -> list[StatisticResponse]:
        response = self.client.get_statistic_api(item_id)
        return [StatisticResponse.model_validate(item) for item in response.json()]
