from typing import Union, Dict

from fastapi import APIRouter

from .dto.item_dto import ItemDto

router = APIRouter()


@router.get("/items/{item_id}")
def get_item(item_id: int, q: Union[str, None] = None) -> Dict[str, Union[str, int, None]]:
    return {"item_id": item_id, "q": q}


@router.put("/items/{item_id}")
def update_item(item_id: int, item: ItemDto) -> Dict[str, Union[str, int, float]]:
    return {"item_name": item.name, "item_id": item_id, "item_price": item.price}
