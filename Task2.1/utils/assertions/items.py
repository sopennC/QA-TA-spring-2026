from requests import Response

from models.items import CreateItemResponse, ErrorResponse, ItemResponse, StatisticResponse


def assert_create_success(response: Response) -> CreateItemResponse:
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    assert "application/json" in response.headers.get("Content-Type", "")
    result = CreateItemResponse.model_validate(response.json())
    assert " - " in result.status, f"UUID not found in status: {result.status}"
    return result


def assert_error_400(response: Response) -> ErrorResponse:
    assert response.status_code == 400, f"Expected 400, got {response.status_code}: {response.text}"
    result = ErrorResponse.model_validate(response.json())
    assert result.result.message
    return result


def assert_not_found(response: Response):
    assert response.status_code == 404, f"Expected 404, got {response.status_code}: {response.text}"


def assert_item_fields(item: ItemResponse, name: str, price: int, seller_id: int):
    assert item.name == name
    assert item.price == price
    assert item.seller_id == seller_id


def assert_stats_valid(stat: StatisticResponse):
    assert stat.view_count >= 0
    assert stat.contacts >= 0
    assert stat.likes >= 0
