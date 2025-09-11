import sys
from typing import Callable, Awaitable

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute

from app.adapter.mongo_adapter import get_item_by_id
from app.domain.item_service import ItemService
from app.domain.item_service_protocol import ItemServiceProtocol
from .rest import items_routes

is_dev = "dev" in sys.argv

app = FastAPI(
    docs_url="/docs" if is_dev else None,
    redoc_url="/redoc" if is_dev else None,
    openapi_url="/openapi.json" if is_dev else None,
)

app.include_router(items_routes.router)

for route in app.routes:
    if isinstance(route, APIRoute):
        route.response_class = JSONResponse


def item_service_provider() -> ItemServiceProtocol:
    return ItemService(get_item_by_id_provider=get_item_by_id)


app.dependency_overrides[ItemService] = item_service_provider


@app.middleware("http")
async def enforce_json_accept(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    accept = request.headers.get("accept", "")
    if "application/json" not in accept and "*/*" not in accept:
        return JSONResponse(
            status_code=406,
            content={"detail": "Not Acceptable"},
        )
    return await call_next(request)
