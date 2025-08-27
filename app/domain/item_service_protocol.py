from __future__ import annotations

from typing import Protocol, runtime_checkable

from .model.item import Item


@runtime_checkable
class ItemServiceProtocol(Protocol):
    def get_item_by_id(self, item_id: int) -> Item | None: ...
