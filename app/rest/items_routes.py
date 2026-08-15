from fastapi import APIRouter, Depends, status
from starlette.responses import JSONResponse

from app.domain.errors import InvalidItemIdError
from app.domain.item_service import ItemService
from app.domain.item_service_protocol import ItemServiceProtocol
from app.domain.model.new_item import NewItem
from .dto.item_dto import ItemDto, NewItemDto

router = APIRouter()


@router.get("/items/{item_id}", response_model=ItemDto)
def get_item(
    item_id: str,
    item_service: ItemServiceProtocol = Depends(ItemService),
):
    try:
        item = item_service.get_item_by_id(item_id)
    except InvalidItemIdError:
        return JSONResponse(status_code=400, content={"detail": "Bad Request"})
    except Exception:
        return JSONResponse(
            status_code=500, content={"detail": "Internal Server Error"}
        )

    if item is None:
        return JSONResponse(status_code=404, content={})

    return ItemDto(id=item.id, name=item.name, price=item.price)


@router.post("/items", response_model=ItemDto, status_code=status.HTTP_201_CREATED)
def create_item(
    new_item_dto: NewItemDto,
    item_service: ItemServiceProtocol = Depends(ItemService),
):
    try:
        item = item_service.create_item(
            NewItem(name=new_item_dto.name, price=new_item_dto.price)
        )
    except Exception:
        return JSONResponse(
            status_code=500, content={"detail": "Internal Server Error"}
        )

    return ItemDto(id=item.id, name=item.name, price=item.price)


@router.put("/items/{item_id}")
def update_item(item_id: str, item: NewItemDto) -> dict[str, float | int | str]:
    return {"item_name": item.name, "item_id": item_id, "item_price": item.price}
