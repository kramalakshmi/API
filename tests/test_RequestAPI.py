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

### Key Points:
- We use `@patch` to mock the HTTP requests made by the `requests` library methods (`get`, `post`, `put`, `delete`).
- Each test checks that the respective method was called with the expected URL and parameters.
- In `test_post_request`, we assert that the returned `user_id` matches the mock data defined.
- Similarly, you can run these tests using the command line by executing `pytest <filename>.py`, where `<filename>.py` is the name of your Python file containing these tests.

Make sure to adjust the import statements and structure of the tests according to your actual module names.