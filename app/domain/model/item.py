from dataclasses import dataclass


@dataclass
class Item:
    item_id: int
    name: str
    price: float
