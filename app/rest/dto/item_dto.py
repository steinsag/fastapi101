from pydantic import BaseModel


class ItemDto(BaseModel):
    id: str
    name: str
    price: float


class NewItemDto(BaseModel):
    name: str
    price: float
