To create unit tests for the provided Python code using `pytest`, we can use the `unittest.mock` module to mock the `requests` library's functions. This way, we can simulate various API responses without making actual network requests. Below are the unit tests for the code provided:

```python
import pytest
from unittest.mock import patch, Mock
import requests

# Assuming the original code is in a module named api_client (you can change this to the actual module name)
from api_client import get_request, post_request, put_request, delete_request

# Test URL and Auth Token
BASE_URL = "https://gorest.co.in"
AUTH_TOKEN = "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"

def test_get_request_success():
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": 1, "name": "John Doe"}]
        mock_get.return_value = mock_response
        
        get_request()  # Call the function
        
        mock_get.assert_called_once_with(f"{BASE_URL}/public/v2/users", headers={"Authorization": AUTH_TOKEN})


def test_post_request_success():
    with patch('requests.post') as mock_post:
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"id": 1, "name": "Naveena"}
        mock_post.return_value = mock_response
        
        user_id = post_request()  # Call the function
        
        assert user_id == 1
        mock_post.assert_called_once_with(
            f"{BASE_URL}/public/v2/users",
            json={"name": "Naveena", "email": "naveean@aa.com", "gender": "male", "status": "active"},
            headers={"Authorization": AUTH_TOKEN}
        )


def test_put_request_success():
    user_id = 1
    with patch('requests.put') as mock_put:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": user_id, "status": "inactive"}
        mock_put.return_value = mock_response
        
        put_request(user_id)  # Call the function
        
        mock_put.assert_called_once_with(
            f"{BASE_URL}/public/v2/users/{user_id}",
            json={"name": "Naveena", "email": "naveena@aa.com", "gender": "male", "status": "inactive"},
            headers={"Authorization": AUTH_TOKEN}
        )


def test_delete_request_success():
    user_id = 1
    with patch('requests.delete') as mock_delete:
        mock_response = Mock()
        mock_response.status_code = 204
        mock_delete.return_value = mock_response
        
        delete_request(user_id)  # Call the function
        
        mock_delete.assert_called_once_with(f"{BASE_URL}/public/v2/users/{user_id}", headers={"Authorization": AUTH_TOKEN})


if __name__ == "__main__":
    pytest.main()
```

### Explanation of the Test Code:
1. **Imports**: We import `pytest` for testing, `patch` and `Mock` for mocking the requests, and the functions we want to test from the module where they are defined.
  
2. **Test Functions**:
   - Each test function simulates a successful call to the corresponding API method (GET, POST, PUT, DELETE).
   - We use `patch` to mock `requests.get`, `requests.post`, `requests.put`, and `requests.delete` calls within their respective test functions.
   - `Mock` objects are constructed to specify the desired behavior of the mocked functions, particularly their `status_code` and `json()` return value.

3. **Assertions**: We make assertions to ensure:
   - The correct user IDs are returned from the `post_request`.
   - The mocked functions are called with the expected arguments.

### Usage:
To run these tests, save them in a file (e.g., `test_api_client.py`), and run the following command in your terminal:
```bash
pytest test_api_client.py
