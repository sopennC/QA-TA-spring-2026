from clients.http_client import HTTPClient
from settings import base_settings


def get_http_client() -> HTTPClient:
    return HTTPClient(
        base_url=base_settings.base_url,
        headers={"User-Agent": "TestClient/1.0"},
    )
