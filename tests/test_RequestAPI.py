To create unit tests for the provided Python code using `pytest`, it's important to keep in mind to focus on testing the functionality of each request method (GET, POST, PUT, and DELETE). Additionally, since the code interacts with an external API, we should use mocking to simulate the API responses, allowing us to perform tests without making actual HTTP requests.

We will use the `pytest` and `unittest.mock` modules to create test cases for the functions. Each test case will verify that the functions behave correctly when provided with deterministic input and handles responses as expected.

Here's how you could structure your test code:

```python
import pytest
from unittest import mock
import requests
from your_module import get_request, post_request, put_request, delete_request  # replace 'your_module' with the actual name of your Python file

# Mock responses for the API calls
mock_get_response = mock.Mock()
mock_post_response = mock.Mock()
mock_put_response = mock.Mock()
mock_delete_response = mock.Mock()

# Setup the mocks for the different methods
def setup_module(module):
    mock_get_response.status_code = 200
    mock_get_response.json.return_value = [{"id": 1, "name": "User"}]

    mock_post_response.status_code = 201
    mock_post_response.json.return_value = {"id": 2, "name": "Naveena"}
    
    mock_put_response.status_code = 200
    mock_put_response.json.return_value = {"id": 2, "name": "Naveena", "status": "inactive"}

    mock_delete_response.status_code = 204

# Test for GET request
@mock.patch('requests.get', return_value=mock_get_response)
def test_get_request(mock_get):
    get_request()
    mock_get.assert_called_once()
    assert mock_get_response.status_code == 200

# Test for POST request
@mock.patch('requests.post', return_value=mock_post_response)
def test_post_request(mock_post):
    user_id = post_request()
    mock_post.assert_called_once()
    assert user_id == 2
    assert mock_post_response.status_code == 201

# Test for PUT request
@mock.patch('requests.put', return_value=mock_put_response)
def test_put_request(mock_put):
    user_id = 2
    put_request(user_id)
    mock_put.assert_called_once_with(f"https://gorest.co.in/public/v2/users/{user_id}", json=mock.ANY, headers=mock.ANY)
    assert mock_put_response.status_code == 200

# Test for DELETE request
@mock.patch('requests.delete', return_value=mock_delete_response)
def test_delete_request(mock_delete):
    user_id = 2
    delete_request(user_id)
    mock_delete.assert_called_once_with(f"https://gorest.co.in/public/v2/users/{user_id}", headers=mock.ANY)
    assert mock_delete_response.status_code == 204

# To run the tests, use the command: pytest <filename>.py in the terminal.
```

### Key Points:
1. **Mocking:** We utilize `unittest.mock.Mock` to create mock responses that simulate the behavior of the `requests` library without actually hitting the URL.
2. **Deterministic Test Cases:** Each test case has a clear expectation based on the mock responses.
3. **Assertions:** We make various assertions to ensure that the status codes and return values match our expectations.
4. **Module Setup:** The function `setup_module` initializes the mock responses, creating a clean context for your tests.

Make sure to replace `'your_module'` with the actual name of the Python file where your functions are defined. 

Lastly, to run your tests, you'll need to have `pytest` installed. You can run your tests using the command: `pytest <filename>.py` in your terminal.