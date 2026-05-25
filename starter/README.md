# Udatracker Starter Code

This directory contains the starter code for the Udatracker project. The initial structure of directories and files is described below.

```
.
├── backend
│   ├── __init__.py
│   ├── app.py
│   ├── in_memory_storage.py
│   ├── order_tracker.py
│   ├── requirements.txt
│   └── tests
│       ├── __init__.py
│       ├── test_api.py
│       └── test_order_tracker.py
├── frontend
│   ├── css
│   │   └── style.css
│   ├── index.html
│   └── js
│       └── script.js
├── pytest.ini
└── README.md
```

### Reflection

#### Trade-offs

* In-memory dictionary storage (InMemoryStorage). This makes testing really fast and reduces the risk of race conditions since they get clear on each run. But it has the disadvantages of the data not persisted when the application restarts and also doesn't allow horizontal scaling of the service. 
* API uses request json bodies that doesn't have any schema definition or validation. This simplifies API implementation and requirements for dependencies. This design is kept to keep compatibility with the Udacity workspace. Although that can be solved with adding dependencies to requirements.txt.
* `uv` has been added as an optional way to run the app or tests by using pyproject.toml dependencies to create a virtual environment and auto install the dependencies. 

#### Testing Insight

* In writing tests for validating status in orders, it was found that different casing for status might be sent via the API. Some endpoints like filter are modified to make sure all status values are lower cases. In real-life implementation, these can be enums or normalizations should be done for all storage or query operations of such values.
* As tests were added for missing orders in the different endpoints of the API. It was observed that error handling in the APIs were duplicated in multiple locations. A better approach was to create errorhandlers.

### Next-step improvement

* Schema for API endpoint request/ response, currently the request json body is being used. A better approach will be to add libraries Pydantic models to the endpoints for request or response. This will also allow integration to OpenAPI libraries to autogenerate documentation. 
* InMemoryStorage is a good start but is not suitable for production usage. Adding persistent storage like MySQL or PostgresSQL will be required if this is a production application. The flaw will be testing will become more complex. That can be solved by adding TestContainers and dependency injection.