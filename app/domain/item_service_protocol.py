from __future__ import annotations

from typing import Protocol, runtime_checkable

from .model.item import Item
from .model.new_item import NewItem


@runtime_checkable
class ItemServiceProtocol(Protocol):
    def get_item_by_id(self, item_id: str) -> Item | None: ...
    def create_item(self, new_item: NewItem) -> Item: ...
