from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Category(Enum):
    COFFEE = "กาแฟ"
    TEA = "ชา"
    SNACK = "ของว่าง"


@dataclass
class MenuItem(ABC):
    name: str
    price: float
    category: Category
    image_path: Optional[str] = None

    def __post_init__(self):
        self._validate_price()

    def _validate_price(self) -> None:
        if self.price < 0:
            raise ValueError("Price must be non-negative")

    @abstractmethod
    def get_display_price(self) -> str:
        pass

    def __str__(self) -> str:
        return f"{self.name} - ฿{self.price:.1f}"


class Beverage(MenuItem):
    def __init__(self, name: str, price: float, category: Category = Category.COFFEE, 
                 image_path: Optional[str] = None, size: str = "M"):
        super().__init__(name, price, category, image_path)
        self._size = size

    def get_display_price(self) -> str:
        return f"฿{self.price:.1f}"


class Snack(MenuItem):
    def __init__(self, name: str, price: float, category: Category = Category.SNACK,
                 image_path: Optional[str] = None):
        super().__init__(name, price, category, image_path)

    def get_display_price(self) -> str:
        return f"฿{self.price:.1f}"


def create_menu_item(item_type: str, name: str, price: float, 
                    category: Category, **kwargs) -> MenuItem:
    if item_type == "beverage":
        return Beverage(name, price, category, **kwargs)
    elif item_type == "snack":
        return Snack(name, price, category, **kwargs)
    raise ValueError(f"Unknown item type: {item_type}")
