import allure
import requests
from requests import Response


class HTTPClient:
    def __init__(self, base_url: str, headers: dict | None = None):
        self.session = requests.Session()
        self.base_url = base_url
        self.session.headers.update(headers or {})

    def _attach_response(self, response: Response):
        allure.attach(
            f"{response.request.method} {response.url}\nStatus: {response.status_code}\nBody: {response.text[:1000]}",
            name=f"{response.request.method} {response.status_code}",
            attachment_type=allure.attachment_type.TEXT,
        )

    @allure.step("GET {path}")
    def get(self, path: str, **kwargs) -> Response:
        response = self.session.get(f"{self.base_url}{path}", **kwargs)
        self._attach_response(response)
        return response

    @allure.step("POST {path}")
    def post(self, path: str, **kwargs) -> Response:
        response = self.session.post(f"{self.base_url}{path}", **kwargs)
        self._attach_response(response)
        return response
