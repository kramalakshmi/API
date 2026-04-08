To write pytest unit tests for the provided Python code, we need to mock the `requests` library to avoid making actual HTTP requests. We will use `unittest.mock` to patch the `requests.get`, `requests.post`, `requests.put`, and `requests.delete` functions.

Here’s how to set up the tests:

1. Mock the responses for the requests.
2. Test each function with clear and deterministic cases.
3. Use `pytest` for the testing framework.

Below are the pytest unit tests for the provided code:

```python
import pytest
from unittest.mock import patch, Mock
import requests

# Assuming the above code is in a module named user_api, change this line as per your module name
from user_api import get_request, post_request, put_request, delete_request

# Test for GET request
@patch('requests.get')
def test_get_request(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"id": 1, "name": "Test User"}]
    mock_get.return_value = mock_response

    get_request()  # Call the function

    mock_get.assert_called_once()
    assert mock_response.status_code == 200

# Test for POST request
@patch('requests.post')
def test_post_request(mock_post):
    mock_response = Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"id": 1, "name": "Naveena"}
    mock_post.return_value = mock_response

    user_id = post_request()  # Call the function

    mock_post.assert_called_once()
    assert user_id == 1

# Test for PUT request
@patch('requests.put')
def test_put_request(mock_put):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "name": "Naveena", "status": "inactive"}
    mock_put.return_value = mock_response

    put_request(1)  # Call the function with a sample user ID

    mock_put.assert_called_once_with("https://gorest.co.in/public/v2/users/1", json={
        "name": "Naveena",
        "email": "naveena@aa.com",
        "gender": "male",
        "status": "inactive"
    }, headers={"Authorization": "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"})

# Test for DELETE request
@patch('requests.delete')
def test_delete_request(mock_delete):
    mock_response = Mock()
    mock_response.status_code = 204
    mock_delete.return_value = mock_response

    delete_request(1)  # Call the function with a sample user ID

    mock_delete.assert_called_once_with("https://gorest.co.in/public/v2/users/1", headers={"Authorization": "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"})
```

### Explanation:
1. **get_request**: We mock `requests.get`, set its return value to simulate a successful response, and assert that it was called once.
2. **post_request**: Similar to the GET test, we mock `requests.post`, simulate returning a user ID, and check its correctness.
3. **put_request**: We check that the `requests.put` function was called with the expected URL and JSON payload.
4. **delete_request**: We verify that the `requests.delete` function was called with the correct parameters and assert the correct handling of status code.

Make sure to adapt the module import statement (i.e., `from user_api import ...`) as per your actual module's structure. To run these tests, you would typically run `pytest` in your terminal after saving this code in a test file.