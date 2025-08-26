from typing import Union

from pydantic import BaseModel


class ItemDto(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None
