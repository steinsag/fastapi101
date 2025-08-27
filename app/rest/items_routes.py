from typing import Dict

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from app.domain.item_service import ItemService
from app.domain.item_service_protocol import ItemServiceProtocol
from .dto.item_dto import ItemDto

router = APIRouter()


@router.get("/items/{item_id}", response_model=ItemDto)
def get_item(
    item_id: int,
    item_service: ItemServiceProtocol = Depends(ItemService),
):
    try:
        item = item_service.get_item_by_id(item_id)
    except Exception:
        return JSONResponse(
            status_code=500, content={"detail": "Internal Server Error"}
        )

    if item is None:
        return JSONResponse(status_code=404, content={})

    return ItemDto(name=item.name, price=item.price)


@router.put("/items/{item_id}")
def update_item(item_id: int, item: ItemDto) -> Dict[str, float | int | str]:
    return {"item_name": item.name, "item_id": item_id, "item_price": item.price}
