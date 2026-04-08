To generate pytest unit tests for the provided Python code, we can use the `unittest.mock` library to mock the `requests` module. This allows us to simulate the API responses without making actual HTTP requests. Below are pytest unit tests that cover the four functions: `get_request`, `post_request`, `put_request`, and `delete_request`.

```python
import pytest
from unittest.mock import patch, MagicMock
import requests
from your_module import get_request, post_request, put_request, delete_request  # Adjust import based on your module name

# Test for the GET request function
@patch('requests.get')
def test_get_request(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": []}
    mock_get.return_value = mock_response

    get_request()  # Call the function to test

    mock_get.assert_called_once()
    assert mock_get.call_args[1]['headers']['Authorization'] == "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"


# Test for the POST request function
@patch('requests.post')
def test_post_request(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"id": 12345}
    mock_post.return_value = mock_response

    user_id = post_request()  # Call the function to test

    mock_post.assert_called_once()
    assert user_id == 12345
    assert mock_post.call_args[1]['headers']['Authorization'] == "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"


# Test for the PUT request function
@patch('requests.put')
def test_put_request(mock_put):
    user_id = 12345
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    mock_put.return_value = mock_response

    put_request(user_id)  # Call the function to test

    mock_put.assert_called_once_with(f'https://gorest.co.in/public/v2/users/{user_id}', json={
        "name": "Naveena",
        "email": "naveena@aa.com",
        "gender": "male",
        "status": "inactive"
    }, headers={"Authorization": "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"})


# Test for the DELETE request function
@patch('requests.delete')
def test_delete_request(mock_delete):
    user_id = 12345
    mock_response = MagicMock()
    mock_response.status_code = 204
    mock_delete.return_value = mock_response

    delete_request(user_id)  # Call the function to test

    mock_delete.assert_called_once()
    assert mock_delete.call_args[1]['headers']['Authorization'] == "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"


if __name__ == "__main__":
    pytest.main()
```

In this test suite, we use the `patch` decorator to replace the actual `requests.get`, `requests.post`, `requests.put`, and `requests.delete` calls with mocks. We create mock responses for each type of request, asserting that the functions behave correctly based on those responses.

### Note:
1. Replace `from your_module import ...` with the actual module name where your functions are defined.
2. The tests cover both the functionality and verify that the correct headers are being sent in the requests.
3. Make sure to have `pytest` and `unittest.mock` installed and accessible in your environment to run these tests.