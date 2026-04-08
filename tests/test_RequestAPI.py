Here's how you can generate unit tests for the provided functions in the Python code using the `pytest` framework. To simulate HTTP responses, we'll use the `requests` library's mocking feature via the `pytest-mock` plugin or `unittest.mock`. Here are the tests for the `get_request`, `post_request`, `put_request`, and `delete_request` functions:

### Pytest Unit Tests

```python
import pytest
from unittest.mock import patch
import requests

# Importing the functions from the provided code (assuming it's in a module named `api_module`)
from api_module import get_request, post_request, put_request, delete_request

@pytest.fixture
def mock_requests():
    with patch('requests.get') as mock_get, \
         patch('requests.post') as mock_post, \
         patch('requests.put') as mock_put, \
         patch('requests.delete') as mock_delete:
        yield mock_get, mock_post, mock_put, mock_delete

def test_get_request(mock_requests):
    mock_get, _, _, _ = mock_requests
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{"id": 1, "name": "John Doe"}]
    
    get_request()  # Call the function
    
    mock_get.assert_called_once()  # Check if requests.get was called

def test_post_request(mock_requests):
    _, mock_post, _, _ = mock_requests
    mock_post.return_value.status_code = 201
    mock_post.return_value.json.return_value = {"id": 1, "name": "Naveena"}
    
    user_id = post_request()  # Call the function
    
    assert user_id == 1  # Verify if the returned user_id is correct
    mock_post.assert_called_once()  # Check if requests.post was called

def test_put_request(mock_requests):
    _, _, mock_put, _ = mock_requests
    mock_put.return_value.status_code = 200
    mock_put.return_value.json.return_value = {"id": 1, "name": "Naveena", "status": "inactive"}
    
    put_request(1)  # Call the function
    
    mock_put.assert_called_once()  # Check if requests.put was called

def test_delete_request(mock_requests):
    _, _, _, mock_delete = mock_requests
    mock_delete.return_value.status_code = 204
    
    delete_request(1)  # Call the function
    
    mock_delete.assert_called_once()  # Check if requests.delete was called

```

### How to Run Tests

1. **Install Required Packages**: Ensure you have `pytest` and `pytest-mock` installed. You can install them with pip if necessary:

   ```bash
   pip install pytest pytest-mock
   ```

2. **Save the Tests**: Save the above test code in a file named `test_api_module.py` (matching the name of your module).

3. **Run Tests**: Execute the tests using pytest from the command line:

   ```bash
   pytest test_api_module.py
   ```

### Explanation of Tests

1. **test_get_request**: Mocks the GET request, simulates a successful response with a 200 status code, and checks whether `requests.get` was called.

2. **test_post_request**: Mocks the POST request, simulates a successful creation with a 201 status code and checks if the returned user ID is correct.

3. **test_put_request**: Mocks the PUT request, simulates a successful update with a 200 status code and verifies the call to `requests.put`.

4. **test_delete_request**: Mocks the DELETE request, simulates successful deletion with a 204 status code and verifies the call to `requests.delete`.

### Notes

- The `mock_requests` fixture creates mock objects for all request methods that are used in the functions.
- Each test focuses on a specific function to ensure that the function behaves correctly when called, without making actual HTTP requests.
- Exit cleanly from tests with proper assertions and verification of method calls.