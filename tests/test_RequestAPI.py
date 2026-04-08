To write unit tests for the provided Python code using `pytest`, we will need to mock the `requests` library since we don't want to make actual HTTP calls while testing. We'll use the `unittest.mock` library to achieve this. This approach lets us simulate different responses for the HTTP requests.

Below are the unit tests for the provided code, using clear and deterministic test cases.

```python
import pytest
from unittest.mock import patch, Mock
from mymodule import get_request, post_request, put_request, delete_request  # Assuming your code is in mymodule.py

# Replace with the actual base_url and auth_token if you need specific tests
base_url = "https://gorest.co.in"
auth_token = "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"

# Mock data for user
mock_user_data = {
    "id": 1,
    "name": "Naveena",
    "email": "naveena@aa.com",
    "gender": "male",
    "status": "active"
}


@patch('requests.get')
def test_get_request(mock_get):
    # Arrange
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [mock_user_data]
    mock_get.return_value = mock_response
    
    # Act
    get_request()
    
    # Assert
    mock_get.assert_called_once_with(f"{base_url}/public/v2/users", headers={"Authorization": auth_token})


@patch('requests.post')
def test_post_request(mock_post):
    # Arrange
    mock_response = Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = mock_user_data
    mock_post.return_value = mock_response

    # Act
    user_id = post_request()

    # Assert
    mock_post.assert_called_once_with(f"{base_url}/public/v2/users", json={
        "name": "Naveena",
        "email": "naveean@aa.com",
        "gender": "male",
        "status": "active"
    }, headers={"Authorization": auth_token})
    assert user_id == mock_user_data["id"]


@patch('requests.put')
def test_put_request(mock_put):
    # Arrange
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_user_data
    mock_put.return_value = mock_response

    # Act
    put_request(mock_user_data["id"])

    # Assert
    mock_put.assert_called_once_with(f"{base_url}/public/v2/users/{mock_user_data['id']}", json={
        "name": "Naveena",
        "email": "naveena@aa.com",
        "gender": "male",
        "status": "inactive"
    }, headers={"Authorization": auth_token})


@patch('requests.delete')
def test_delete_request(mock_delete):
    # Arrange
    mock_response = Mock()
    mock_response.status_code = 204
    mock_delete.return_value = mock_response

    # Act
    delete_request(mock_user_data["id"])

    # Assert
    mock_delete.assert_called_once_with(f"{base_url}/public/v2/users/{mock_user_data['id']}", headers={"Authorization": auth_token})


# To run the tests, you would typically run: pytest <filename>.py in terminal
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
