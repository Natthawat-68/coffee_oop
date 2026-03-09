from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from .menu import MenuItem


@dataclass
class OrderItem:
    menu_item: MenuItem
    quantity: int = 1
    notes: str = ""

    @property
    def subtotal(self) -> float:
        """Encapsulation: คำนวณยอดย่อย"""
        return self.menu_item.price * self.quantity

    def __str__(self) -> str:
        return f"{self.menu_item.name} x{self.quantity}"


@dataclass
class Order:
    items: List[OrderItem] = field(default_factory=list)
    customer_name: str = ""
    table_no: str = ""
    is_dine_in: bool = True
    order_id: int = 0
    created_at: datetime = field(default_factory=datetime.now)

    def add_item(self, menu_item: MenuItem, quantity: int = 1, notes: str = "") -> None:
        for oi in self.items:
            if oi.menu_item.name == menu_item.name and oi.notes == notes:
                oi.quantity += quantity
                return
        self.items.append(OrderItem(menu_item, quantity, notes))

    def remove_item(self, index: int) -> None:
        if 0 <= index < len(self.items):
            self.items.pop(index)

    def update_quantity(self, index: int, quantity: int) -> None:
        if 0 <= index < len(self.items):
            if quantity <= 0:
                self.remove_item(index)
            else:
                self.items[index].quantity = quantity

    @property
    def total(self) -> float:
        return sum(oi.subtotal for oi in self.items)

    def clear(self) -> None:
        self.items.clear()
