from pydantic import BaseModel, ConfigDict, Field


class Statistics(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    likes: int
    view_count: int = Field(alias="viewCount")
    contacts: int


class CreateItemRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    price: int
    seller_id: int = Field(alias="sellerID")
    statistics: Statistics


class ItemResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    name: str
    price: int
    seller_id: int = Field(alias="sellerId")
    statistics: Statistics
    created_at: str = Field(alias="createdAt")


class CreateItemResponse(BaseModel):
    status: str


class StatisticResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    view_count: int = Field(alias="viewCount")
    contacts: int
    likes: int


class ErrorResult(BaseModel):
    message: str
    messages: dict


class ErrorResponse(BaseModel):
    result: ErrorResult
    status: str
