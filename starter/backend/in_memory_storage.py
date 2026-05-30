# This file provides a simple in-memory storage implementation for orders.
# Data stored here will be lost when the application restarts.
class InMemoryStorage:
    """
    A simple in-memory implementation of the storage interface.
    Stores orders in a Python dictionary.
    """
    def __init__(self):
        self._orders = {}

    def save_order(self, order_id: str, order_data: dict) -> dict[str, str | int]:
        self._orders[order_id] = order_data.copy()
        # Making a change to the save method which is a common pattern for
        # storage repository to returned the entity that is saved
        return self._orders[order_id]

    def get_order(self, order_id: str) -> dict[str, str | int] | None:
        return self._orders.get(order_id, {}).copy() if self._orders.get(order_id) else None

    def delete_order(self, order_id: str) -> dict[str, str | int] :
        return self._orders.pop(order_id)

    def get_all_orders(self) -> dict[str, dict[str, str | int]]:
        return {k: v.copy() for k, v in self._orders.items()}

    def clear(self) -> dict:
        self._orders = {}
