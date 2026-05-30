from unittest.mock import Mock

import pytest

from ..order_tracker import OrderTracker

# --- Fixtures for Unit Tests ---

@pytest.fixture
def mock_storage():
    """
    Provides a mock storage object for tests.
    This mock will be configured to simulate various storage behaviors.
    """
    mock = Mock()
    # By default, mock get_order to return None (no order found)
    mock.get_order.return_value = None
    # By default, mock get_all_orders to return an empty dict
    mock.get_all_orders.return_value = {}
    return mock

@pytest.fixture
def order_tracker(mock_storage):
    """
    Provides an OrderTracker instance initialized with the mock_storage.
    """
    return OrderTracker(mock_storage)

#
# --- TODO: add test functions below this line ---
#
def test_add_order_successfully(
    order_tracker: OrderTracker, mock_storage: Mock
):
    """Tests adding a new order with default 'pending' status."""
    order_tracker.add_order("ORD001", "Laptop", 1, "CUST001")

    # We expect save_order to be called once
    mock_storage.save_order.assert_called_once()

def test_add_order_raises_error_if_exists(
    order_tracker: OrderTracker, mock_storage: Mock
):
    """Tests that adding an order with a duplicate ID raises a ValueError"""
    # Simulate that the storage finds an existing order
    mock_storage.get_order.return_value = {
        "order_id": "ORD_EXISTING"
    }
    with pytest.raises(
        ValueError, match="Order with ID 'ORD_EXISTING' already exists."
    ):
        order_tracker.add_order(
            "ORD_EXISTING", "New Item", 1, "CUST001"
        )

@pytest.mark.parametrize(
    "status", [
        (None),
        (""),
        ("unknown"),
    ]
)
def test_add_order_raises_error_if_invalid_status(
    status: str, order_tracker: OrderTracker
):
    """Tests that adding an order with a duplicate ID raises a ValueError"""
    # Simulate that the storage finds an existing order
    with pytest.raises(
        ValueError, match=f"Order with invalid status '{status}'."
    ):
        order_tracker.add_order(
            "ORD_EXISTING", "New Item", 1, "CUST001", status
        )

@pytest.mark.parametrize(
    "quantity", [
        (1.0),
        (0),
        (-1),
        (None),
        (""),
        ("1"),
    ]
)
def test_add_order_raises_error_if_invalid_quantity(
    quantity: float | int | str | None, order_tracker: OrderTracker
):
    """Tests that adding an order with a duplicate ID raises a ValueError"""
    # Simulate that the storage finds an existing order
    with pytest.raises(
        ValueError, match=f"Order with invalid quantity '{quantity}'."
    ):
        order_tracker.add_order(
            "ORD_EXISTING", "New Item", quantity, "CUST001"
        )

def test_get_order_by_id_successfully(
    order_tracker: OrderTracker, mock_storage: Mock
):
    """Tests getting an existing order using an order_id."""
    order_id = "ORD001"
    expected = {
        "order_id": order_id,
        "item_name": "Laptop",
        "quantity": 1,
        "customer_id": "CUST001",
        "status": "pending"
    }
    mock_storage.get_order.return_value = expected
    actual = order_tracker.get_order_by_id(order_id)

    # We expect get_order to be called once
    mock_storage.get_order.assert_called_once_with(order_id=order_id)
    assert actual == expected

def test_get_order_by_id_raises_error_if_not_exists(
    order_tracker: OrderTracker, mock_storage: Mock
):
    """Tests getting a non existing order using an order_id."""
    order_id = "ORD001"
    with pytest.raises(KeyError, match=f"Order '{order_id}' not found"):
        _ = order_tracker.get_order_by_id(order_id)

    # We expect get_order to be called once
    mock_storage.get_order.assert_called_once_with(order_id=order_id)

@pytest.mark.parametrize(
    "old_status, new_status",
    [("processing", "shipped"), ("pending", "processing")]
)
def test_update_order_status_successfully(
    old_status: str, new_status: str, order_tracker: OrderTracker, mock_storage: Mock
):
    """Tests getting an existing order using an order_id."""
    order_id = "ORD001"
    base = {
        "order_id": order_id,
        "item_name": "Laptop",
        "quantity": 1,
        "customer_id": "CUST001",
    }
    expected = {
        **base,
        "status": new_status
    }
    mock_storage.get_order.return_value = {
        **base,
        "status": old_status
    }
    mock_storage.save_order.return_value = expected
    actual = order_tracker.update_order_status(order_id, new_status)

    # We expect save_order to be called once
    mock_storage.get_order.assert_called_once_with(order_id=order_id)
    mock_storage.save_order.assert_called_once_with(
        order_id=order_id,
        order_data=expected
    )
    assert actual == expected

@pytest.mark.parametrize(
    "old_status, new_status",
    [("processing", "unknown"), ("processing", ""), ("processing", None)]
)
def test_update_order_status_with_invalid_status_failure(
    old_status: str, new_status: str | None, order_tracker: OrderTracker, mock_storage: Mock
):
    """Tests getting an existing order using an order_id."""
    order_id = "ORD001"
    base = {
        "order_id": order_id,
        "item_name": "Laptop",
        "quantity": 1,
        "customer_id": "CUST001",
    }
    mock_storage.get_order.return_value = {
        **base,
        "status": old_status
    }

    with pytest.raises(
        ValueError, match=f"Order update with invalid status '{new_status}'"
    ):
        _ = order_tracker.update_order_status(order_id, new_status)

    # We expect save_order to be called once
    mock_storage.get_order.assert_not_called()
    mock_storage.save_order.assert_not_called()

def test_update_order_status_raises_error_if_not_exists(
    order_tracker: OrderTracker, mock_storage: Mock
):
    """Tests getting an existing order using an order_id."""
    order_id = "ORD001"
    mock_storage.get_order.return_value = None

    with pytest.raises(KeyError, match=f"Order '{order_id}' not found"):
        order_tracker.update_order_status(order_id, "shipped")

    mock_storage.save_order.assert_not_called()


"""
    Orders in this section is not placed into fixtures due as tests are typically fixed and not changed after released.
    Test data placed directly in the test makes the intention of the tests clearer.
"""

@pytest.mark.parametrize(
    "orders", [
        ({
            "ORD001": {
                "order_id": "ORD001",
                "item_name": "Laptop",
                "quantity": 1,
                "customer_id": "CUST001",
                "status": "pending"
            },
            "ORD002": {
                "order_id": "ORD002",
                "item_name": "Mobile Phone",
                "quantity": 1,
                "customer_id": "CUST002",
                "status": "shipped"
            },
            "ORD003": {
                "order_id": "ORD003",
                "item_name": "Laptop",
                "quantity": 15,
                "customer_id": "CUST0012",
                "status": "shipped"
            },
        }),
        ({})
    ]
)
def test_list_all_orders_with_orders_successfully(
    orders: dict[str, dict[str, str | int]], order_tracker: OrderTracker, mock_storage: Mock
):
    """Tests getting all orders."""
    expected = orders
    mock_storage.get_all_orders.return_value = orders

    actual = order_tracker.list_all_orders()

    # We expect get_all_orders to be called once
    mock_storage.get_all_orders.assert_called_once()
    assert actual == expected

@pytest.mark.parametrize(
    "orders", [
        ({
            "ORD001": {
                "order_id": "ORD001",
                "item_name": "Laptop",
                "quantity": 1,
                "customer_id": "CUST001",
                "status": "pending"
            },
            "ORD002": {
                "order_id": "ORD002",
                "item_name": "Mobile Phone",
                "quantity": 1,
                "customer_id": "CUST002",
                "status": "pending"
            }
        })
    ]
)
def test_list_orders_by_status_all_found_successfully(
    orders: dict[str, dict[str, str | int]],
    order_tracker: OrderTracker,
    mock_storage: Mock
):
    """Tests getting orders by status all found."""
    expected = orders
    mock_storage.get_all_orders.return_value = orders

    actual = order_tracker.list_orders_by_status(status="pending")

    # We expect get_all_orders to be called once
    mock_storage.get_all_orders.assert_called_once()
    assert actual == expected

@pytest.mark.parametrize(
    "orders, expected", [
        ({
            "ORD001": {
                "order_id": "ORD001",
                "item_name": "Laptop",
                "quantity": 1,
                "customer_id": "CUST001",
                "status": "pending"
            },
            "ORD002": {
                "order_id": "ORD002",
                "item_name": "Mobile Phone",
                "quantity": 1,
                "customer_id": "CUST002",
                "status": "shipped"
            },
            "ORD003": {
                "order_id": "ORD003",
                "item_name": "Laptop",
                "quantity": 15,
                "customer_id": "CUST0012",
                "status": "shipped"
            },
        }, {
            "ORD002": {
                "order_id": "ORD002",
                "item_name": "Mobile Phone",
                "quantity": 1,
                "customer_id": "CUST002",
                "status": "shipped"
            },
            "ORD003": {
                "order_id": "ORD003",
                "item_name": "Laptop",
                "quantity": 15,
                "customer_id": "CUST0012",
                "status": "shipped"
            },
        })
    ]
)
def test_list_orders_by_status_partial_found_successfully(
    orders: dict[str, dict[str, str | int]],
    expected: dict[str, dict[str, str | int]],
    order_tracker: OrderTracker,
    mock_storage: Mock
):
    """Tests getting orders by status filtered partial."""
    mock_storage.get_all_orders.return_value = orders

    actual = order_tracker.list_orders_by_status(status="shipped")

    # We expect get_all_orders to be called once
    mock_storage.get_all_orders.assert_called_once()
    assert actual == expected

@pytest.mark.parametrize(
    "orders", [
        ({
            "ORD001": {
                "order_id": "ORD001",
                "item_name": "Laptop",
                "quantity": 1,
                "customer_id": "CUST001",
                "status": "pending"
            },
            "ORD002": {
                "order_id": "ORD002",
                "item_name": "Mobile Phone",
                "quantity": 1,
                "customer_id": "CUST002",
                "status": "pending"
            }
        })
    ]
)
def test_list_orders_by_status_not_found_successfully(
    orders: dict[str, dict[str, str | int]],
    order_tracker: OrderTracker,
    mock_storage: Mock
):
    """Tests getting orders by status not found."""
    expected = {}
    mock_storage.get_all_orders.return_value = orders

    actual = order_tracker.list_orders_by_status(status="shipping")

    # We expect get_all_orders to be called once
    mock_storage.get_all_orders.assert_called_once()
    assert actual == expected

@pytest.mark.parametrize(
    "status", [
        ("pending"),
        ("Pending"),
        ("PENDING")
    ]
)
def test_list_orders_by_status_all_found_status_casing_successfully(
    status: str,
    order_tracker: OrderTracker,
    mock_storage: Mock
):
    """Tests getting orders by status with different casing all found."""
    orders = {
        "ORD001": {
            "order_id": "ORD001",
            "item_name": "Laptop",
            "quantity": 1,
            "customer_id": "CUST001",
            "status": "pending"
        },
        "ORD002": {
            "order_id": "ORD002",
            "item_name": "Mobile Phone",
            "quantity": 1,
            "customer_id": "CUST002",
            "status": "pending"
        }
    }
    expected = orders
    mock_storage.get_all_orders.return_value = orders

    actual = order_tracker.list_orders_by_status(status=status)

    # We expect get_all_orders to be called once
    mock_storage.get_all_orders.assert_called_once()
    assert actual == expected

@pytest.mark.parametrize("status", [
    (None),
    ("")
])
def test_list_orders_by_status_bad_status_failure(
    status: str,
    order_tracker: OrderTracker,
    mock_storage: Mock
):
    """
        Tests getting orders by bad status raises error.
        Take note that this is not all comprehensive and just an example of the what can be done.
    """
    with pytest.raises(
        ValueError,
        match=f"Order list with invalid status '{status}'"
    ):
        order_tracker.list_orders_by_status(status=status)

    # We expect get_all_orders to be called not called
    mock_storage.get_all_orders.assert_not_called()

def test_delete_order_successfully(
    order_tracker: OrderTracker, mock_storage: Mock
):
    """Tests deleting an order with order_id."""
    order_id = "ORD001"
    item = {
        "order_id": order_id,
        "item_name": "Laptop",
        "quantity": 1,
        "customer_id": "CUST001",
        "status": "pending"
    }
    expected = item
    mock_storage.delete_order.return_value = item

    actual = order_tracker.delete_order(order_id)

    # We expect delete_order to be called once
    mock_storage.delete_order.assert_called_once_with(order_id=order_id)
    assert actual == expected

def test_delete_order_with_invalid_order_failure(
    order_tracker: OrderTracker, mock_storage: Mock
):
    """Tests deleting an order with order_id."""
    order_id = "ORD001"
    mock_storage.delete_order.side_effect = ValueError(f"Order '{order_id}' not found")

    with pytest.raises(ValueError, match=f"Order '{order_id}' not found"):
        _ = order_tracker.delete_order(order_id)

    # We expect delete_order to be called once
    mock_storage.delete_order.assert_called_once_with(order_id=order_id)
