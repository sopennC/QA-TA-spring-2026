from enum import Enum


class APIRoutes(str, Enum):
    ITEM = "/api/1/item"
    STATISTIC = "/api/1/statistic"

    def __str__(self) -> str:
        return self.value
