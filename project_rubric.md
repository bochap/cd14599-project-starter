# Project Rubric: Order Tracker & RESTful API

Use this project rubric to understand and assess the project criteria.

---

## 1. Core Order Logic (Unit Tests)

### Order Creation
* **Requirements:**
    * Implement `add_order` method in `OrderTracker`.
    * Write unit tests in `tests/test_order_tracker.py` that verify a new order can be added successfully.
    * Tests must check that the order details (ID, items, customer) are stored correctly and that the initial status defaults to `'pending'`.
    * Include at least one test for invalid input (e.g., duplicate ID, missing required fields, invalid quantity or status). *Note: It’s not necessary to cover all invalid cases.*

### Order Retrieval
* **Requirements:**
    * Implement `get_order_by_id` method.
    * Write unit tests to fetch an existing order by its ID.
    * Write a test to handle cases where the order ID does not exist or is invalid.

### Order Status Update
* **Requirements:**
    * Implement `update_order_status` method.
    * Write unit tests to change an order's status (e.g., from `'pending'` to `'shipped'`).
    * Write tests to handle invalid updates, such as a non-existent order, an invalid status, or an empty order ID.

### List and Filter Orders
* **Requirements:**
    * Implement `list_all_orders` and `list_orders_by_status` methods.
    * Write unit tests to list all current orders.
    * Write unit tests to retrieve only orders with a specific status (e.g., `'shipped'`).

---

## 2. RESTful API Endpoints (Integration Tests)

### Create Order Endpoint (`POST /api/orders`)
* **Requirements:**
    * Implement the API endpoint for creating a new order (`POST /api/orders`).
    * Do not modify or remove the provided tests in `backend/tests/test_api.py`.
    * Ensure the provided integration test passes (it sends a POST with valid data and asserts a `201 Created` response with the order JSON).

### Get Order Endpoint (`GET /api/orders/<order_id>`)
* **Requirements:**
    * Implement the API endpoint for retrieving a single order (`GET /api/orders/<order_id>`).
    * Ensure the provided integration tests in `backend/tests/test_api.py` pass (they fetch a known order and assert a `200 OK` response with the correct JSON).

### Update Order Status Endpoint (`PUT /api/orders/<order_id>`)
* **Requirements:**
    * Implement the API endpoint for updating an order's status (`PUT /api/orders/<order_id>`).
    * Ensure the provided integration test in `backend/tests/test_api.py` passes (it sends a PUT with a new status and asserts a `200 OK` response with the updated JSON).

### List All Orders Endpoint (`GET /api/orders`)
* **Requirements:**
    * Implement the API endpoint for listing all orders (`GET /api/orders`).
    * Ensure the provided integration test in `backend/tests/test_api.py` passes (it asserts `200 OK` and that the returned list includes previously created orders).

---

## 3. TDD Process and Project Structure

### Test-First Approach
* **Requirements:**
    * Include learner-authored unit tests in `backend/tests/test_order_tracker.py` for the `OrderTracker` methods specified in the instructions (`get_order_by_id`, `update_order_status`, `list_all_orders`, `list_orders_by_status`), in addition to the two provided example tests.
    * All tests must pass when run from the project root (`pytest`).

### Code Readability and Structure
* **Requirements:**
    * The project must be well-organized under `backend/`:
        * Business logic in `backend/order_tracker.py`
        * API layer in `backend/app.py`
        * Storage in `backend/in_memory_storage.py`
    * Code must be clean, commented where necessary, and adhere to PEP 8 standards.

### README Reflection
* **Requirements:**
    * `starter/README.md` must contain a short reflection (2–5 bullets or ~80–150 words) that covers at least two of the following topics:
        * A design decision or trade-off you made in `OrderTracker` or the API routes.
        * A testing insight (e.g., a failing test that caught a bug or drove a refactor).
        * A next-step improvement you’d pursue (e.g., DELETE endpoint, persistent storage, stricter validation).

---

## 💡 Suggestions to Make Your Project Stand Out

* **Error Handling:** Return consistent JSON error objects (e.g., `{"error": "message"}`) and appropriate status codes (`400` for validation errors, `404` for not found). Consider a simple Flask error handler to centralize this.
* **Filtering by Customer:** Extend `GET /api/orders` to accept `customer_id` (and optionally combine with status), e.g., `/api/orders?customer_id=C123&status=pending`.
* **Delete Order Endpoint:** Add `DELETE /api/orders/<order_id>` to remove an order. Return `204 No Content` (or `200` with the deleted order) and update tests accordingly.
* **API Documentation:** Add a brief API reference or OpenAPI YAML in `starter/README.md` with sample `curl` commands.
* **Dockerization (for local use):** Provide a lightweight `Dockerfile` for the backend (bind to `0.0.0.0`) and optionally a `docker-compose.yml` if you add services. *Note: The Udacity Workspace already runs in Docker—this is mainly for local development.*
