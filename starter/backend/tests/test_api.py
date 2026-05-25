import pytest
from typing import Any
from backend.app import app, in_memory_storage

@pytest.fixture
def client() -> Any:
    app.config['TESTING'] = True
    app.config['DEBUG'] = False
    in_memory_storage.clear()
    with app.test_client() as client:
        yield client

def test_add_order_api_success(client: Any):
    order_data = {
        "order_id": "API001", "item_name": "API Laptop", "quantity": 1, "customer_id": "APICUST001"
    }
    response = client.post('/api/orders', json=order_data)
    assert response.status_code == 201
    assert response.json['order_id'] == "API001"

def test_get_order_api_success(client: Any):
    client.post('/api/orders', json={
        "order_id": "GET001", "item_name": "Test Item", "quantity": 1, "customer_id": "C1"
    })
    response = client.get('/api/orders/GET001')
    assert response.status_code == 200
    assert response.json['order_id'] == "GET001"

def test_get_order_api_not_found(client: Any):
    response = client.get('/api/orders/NONEXISTENT')
    assert response.status_code == 404

def test_update_order_status_api_success(client: Any):
    client.post('/api/orders', json={
        "order_id": "UPDATE001", "item_name": "Test Item", "quantity": 1, "customer_id": "C1"
    })
    response = client.put('/api/orders/UPDATE001/status', json={"new_status": "shipped"})
    assert response.status_code == 200
    assert response.json['status'] == "shipped"

def test_list_all_orders_api_with_data(client: Any):
    client.post('/api/orders', json={"order_id": "LST001", "item_name": "Item A", "quantity": 1, "customer_id": "C1"})
    client.post('/api/orders', json={"order_id": "LST002", "item_name": "Item B", "quantity": 2, "customer_id": "C2"})
    response = client.get('/api/orders')
    assert response.status_code == 200
    assert len(response.json) == 2

def test_list_orders_by_status_api_matching(client: Any):
    client.post('/api/orders', json={"order_id": "S001", "item_name": "A", "quantity": 1, "customer_id": "C1", "status": "pending"})
    client.post('/api/orders', json={"order_id": "S002", "item_name": "B", "quantity": 2, "customer_id": "C2", "status": "shipped"})
    response = client.get('/api/orders?status=pending')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['order_id'] == "S001"

#
# --- TODO: add new test functions below this line ---
#

def test_get_order_api_invalid_order_failure(client: Any):
    response = client.get('/api/orders/GET001')
    
    assert response.status_code == 404

@pytest.mark.parametrize(
    "quantity", [
        (None),
        (""),
        ("1"),
        (0),
        (-1),
    ]
)
def test_add_order_api_invalid_quantity_failure(
    quantity: float | int | str | None, client: Any
):
    order_data = {
        "order_id": "API001", "item_name": "API Laptop", "quantity": quantity, "customer_id": "APICUST001"
    }
    
    response = client.post('/api/orders', json=order_data)
    
    assert response.status_code == 400

def test_update_order_status_api_bad_status_failure(client: Any):
    client.post('/api/orders', json={
        "order_id": "UPDATE001", "item_name": "Test Item", "quantity": 1, "customer_id": "C1"
    })
    
    response = client.put('/api/orders/UPDATE001/status', json={"new_status": ""})
    
    assert response.status_code == 400

def test_update_order_status_api_invalid_order_failure(client: Any):
    response = client.put('/api/orders/UPDATE001/status', json={"new_status": "shipped"})
    
    assert response.status_code == 404

def test_list_orders_by_status_bad_status_failure(client: Any):
    client.post('/api/orders', json={"order_id": "S001", "item_name": "A", "quantity": 1, "customer_id": "C1", "status": "pending"})
    client.post('/api/orders', json={"order_id": "S002", "item_name": "B", "quantity": 2, "customer_id": "C2", "status": "shipped"})
    
    response = client.get('/api/orders?status=')
    
    assert response.status_code == 400

def test_delete_order_api_successful(client: Any):
    order = {
        "order_id": "DELETE001", "item_name": "Test Item", "quantity": 1, "customer_id": "C1"
    }
    expected = {
        **order,
        "status": "pending"
    }
    client.post('/api/orders', json=order)
    
    response = client.delete('/api/orders/DELETE001')
    
    assert response.status_code == 200
    assert response.json == expected
