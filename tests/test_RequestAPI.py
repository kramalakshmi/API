Sure! Below are some `pytest` unit tests for the given Python code. The tests use `unittest.mock` to mock the requests to the external API, ensuring that our tests are deterministic and isolated from actual external calls.

You will need to add these test cases to a test file, typically named something like `test_your_module.py`, where `your_module` is the name of your Python file containing the code.

```python
import pytest
from unittest.mock import patch, Mock
import requests
from your_module import get_request, post_request, put_request, delete_request  # Replace with your actual module name

# Mocking the base URL for external requests
BASE_URL = "https://gorest.co.in"

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
    # Mock response for GET
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"id": 1, "name": "Test User"}]
    mock_requests_get.return_value = mock_response

    get_request()

    mock_requests_get.assert_called_once()
    assert mock_requests_get.call_args[1]['headers']['Authorization'] == "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"


def test_post_request(mock_requests_post):
    # Mock response for POST
    mock_response = Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"id": 1, "name": "Naveena"}
    mock_requests_post.return_value = mock_response

    user_id = post_request()

    assert user_id == 1
    mock_requests_post.assert_called_once()
    assert mock_requests_post.call_args[1]['headers']['Authorization'] == "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"


def test_put_request(mock_requests_put):
    user_id = 1
    # Mock response for PUT
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "name": "Naveena", "status": "inactive"}
    mock_requests_put.return_value = mock_response

    put_request(user_id)

    mock_requests_put.assert_called_once()
    expected_url = f"{BASE_URL}/public/v2/users/{user_id}"
    assert mock_requests_put.call_args[0][0] == expected_url
    assert mock_requests_put.call_args[1]['headers']['Authorization'] == "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"


def test_delete_request(mock_requests_delete):
    user_id = 1
    # Mock response for DELETE
    mock_response = Mock()
    mock_response.status_code = 204
    mock_requests_delete.return_value = mock_response

    delete_request(user_id)

    mock_requests_delete.assert_called_once()
    expected_url = f"{BASE_URL}/public/v2/users/{user_id}"
    assert mock_requests_delete.call_args[0][0] == expected_url
    assert mock_requests_delete.call_args[1]['headers']['Authorization'] == "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"

```

### Explanation:
1. **Fixtures**: Each fixture patches the corresponding requests method for GET, POST, PUT, and DELETE.
2. **Test Functions**: Each test calls the relevant function and asserts the expected behavior.
3. **Mock Responses**: Mock responses are defined to simulate the behavior of the actual API responses.
4. **Assertions**: We assert that the status codes and URLs received in requests are as expected.
   
Make sure to replace `"your_module"` in the import statement with the actual name of the file where your original code resides. Also, run your tests in an environment where `pytest` is installed.