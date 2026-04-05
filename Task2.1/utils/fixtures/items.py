import pytest

from clients.builder import get_http_client
from clients.items_client import ItemsClient
from managers.items_manager import ItemsManager


@pytest.fixture()
def items_client() -> ItemsClient:
    return ItemsClient(get_http_client())


@pytest.fixture()
def items_manager(items_client: ItemsClient) -> ItemsManager:
    return ItemsManager(items_client)
