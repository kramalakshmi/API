To create `pytest` unit tests for the provided Python code, we'll need to mock the responses from the `requests` library since these are external API calls. We will utilize the `unittest.mock` library for mocking. 

Here's a sample test suite for the provided functions:

```python
import pytest
from unittest.mock import patch, Mock
import json

# Assuming the original code is in a file named api_requests.py
from api_requests import get_request, post_request, put_request, delete_request

# Set a commonly expected auth token for testing
auth_token = "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"

@pytest.fixture
def mock_requests_get():
    with patch('requests.get') as mock_get:
        yield mock_get

@pytest.fixture
def mock_requests_post():
    with patch('requests.post') as mock_post:
        yield mock_post

@pytest.fixture
def mock_requests_put():
    with patch('requests.put') as mock_put:
        yield mock_put

@pytest.fixture
def mock_requests_delete():
    with patch('requests.delete') as mock_delete:
        yield mock_delete


def test_get_request(mock_requests_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"id": 1, "name": "Naveena", "email": "naveean@aa.com"}]
    mock_requests_get.return_value = mock_response

    get_request()
    mock_requests_get.assert_called_once_with("https://gorest.co.in/public/v2/users", headers={"Authorization": auth_token})

def test_post_request(mock_requests_post):
    mock_response = Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"id": 1, "name": "Naveena", "email": "naveean@aa.com"}
    mock_requests_post.return_value = mock_response

    user_id = post_request()
    assert user_id == 1
    mock_requests_post.assert_called_once_with(
        "https://gorest.co.in/public/v2/users",
        json={"name": "Naveena", "email": "naveean@aa.com", "gender": "male", "status": "active"},
        headers={"Authorization": auth_token}
    )

def test_put_request(mock_requests_put):
    user_id = 1
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "name": "Naveena", "email": "naveena@aa.com"}
    mock_requests_put.return_value = mock_response
    
    put_request(user_id)
    mock_requests_put.assert_called_once_with(
        f"https://gorest.co.in/public/v2/users/{user_id}",
        json={"name": "Naveena", "email": "naveena@aa.com", "gender": "male", "status": "inactive"},
        headers={"Authorization": auth_token}
    )

def test_delete_request(mock_requests_delete):
    user_id = 1
    mock_response = Mock()
    mock_response.status_code = 204
    mock_requests_delete.return_value = mock_response
    
    delete_request(user_id)
    mock_requests_delete.assert_called_once_with(
        f"https://gorest.co.in/public/v2/users/{user_id}",
        headers={"Authorization": auth_token}
    )
```

### Explanation
1. **Mocks**: We use `Mock()` to create a mock object for the HTTP response that the `requests` library would normally return. This allows us to simulate different response statuses and data without making actual API calls.

2. **Fixtures**: We create fixtures to initialize our mock objects and patch the respective HTTP methods (`get`, `post`, `put`, `delete`).

3. **Tests**: 
   - `test_get_request`: Validates that the `get_request` function correctly calls the API and handles the response.
   - `test_post_request`: Checks that the `post_request` function returns the expected user ID and makes the correct API call.
   - `test_put_request`: Tests that the `put_request` function behaves as expected for updating user information.
   - `test_delete_request`: Confirms that the `delete_request` function appropriately interacts with the API for user deletion.

You would run these tests using the command `pytest <test_file.py>` in your terminal. If everything is set up correctly and you have `pytest` and `mock` available in your environment, these tests should execute as intended.