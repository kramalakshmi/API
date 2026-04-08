To write unit tests for the given Python code using `pytest`, we can employ the `requests` library along with `unittest.mock` to simulate the HTTP requests and their responses. This allows us to avoid making actual calls to the API and instead test our code logic using mock responses.

Here's how you can structure your `pytest` unit tests for the provided code:

```python
import pytest
from unittest.mock import patch, MagicMock

# Assuming the code is in a module named `api_requests`
# from api_requests import get_request, post_request, put_request, delete_request

base_url = "https://gorest.co.in"
auth_token = "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"

@pytest.fixture
def mock_get_response():
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = [{"id": 1, "name": "User1"}, {"id": 2, "name": "User2"}]
    return response

@pytest.fixture
def mock_post_response():
    response = MagicMock()
    response.status_code = 201
    response.json.return_value = {"id": 123, "name": "Naveena"}
    return response

@pytest.fixture
def mock_put_response():
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {"id": 123, "name": "Naveena", "status": "inactive"}
    return response

@pytest.fixture
def mock_delete_response():
    response = MagicMock()
    response.status_code = 204
    return response

@patch('requests.get')
def test_get_request(mock_get_response):
    mock_get_response.return_value = mock_get_response
    data = get_request()  # replace with the implementation needed

    mock_get_response.assert_called_once_with(base_url + "/public/v2/users", headers={"Authorization": auth_token})

@patch('requests.post')
def test_post_request(mock_post_response):
    mock_post_response.return_value = mock_post_response
    user_id = post_request()  # replace with the implementation needed
    assert user_id == 123  # Test returns user ID correctly

    mock_post_response.assert_called_once_with(
        base_url + "/public/v2/users",
        json={
            "name": "Naveena",
            "email": "naveean@aa.com",
            "gender": "male",
            "status": "active"},
        headers={"Authorization": auth_token}
    )

@patch('requests.put')
def test_put_request(mock_put_response):
    mock_put_response.return_value = mock_put_response
    put_request(123)  # Test with user_id 123

    mock_put_response.assert_called_once_with(
        base_url + "/public/v2/users/123",
        json={
            "name": "Naveena",
            "email": "naveena@aa.com",
            "gender": "male",
            "status": "inactive"},
        headers={"Authorization": auth_token}
    )

@patch('requests.delete')
def test_delete_request(mock_delete_response):
    mock_delete_response.return_value = mock_delete_response
    delete_request(123)  # Test with user_id 123

    mock_delete_response.assert_called_once_with(
        base_url + "/public/v2/users/123",
        headers={"Authorization": auth_token}
    )
```

### Explanation of the Tests:

1. **Fixtures**: 
    - `mock_get_response`: Mocks the response for a GET request scenario.
    - `mock_post_response`: Mocks the response for a POST request scenario.
    - `mock_put_response`: Mocks the response for a PUT request scenario.
    - `mock_delete_response`: Mocks the response for a DELETE request scenario.

2. **Tests**:
    - Each test method uses `@patch` decorator to mock `requests.get`, `requests.post`, `requests.put`, and `requests.delete` as needed.
    - Each test ensures that the appropriate request is made with the correct parameters.
    - The POST test checks if the returned user ID is what we expect from our mock.

### Running Tests:
Ensure you have pytest installed, and then save this code in a separate file (e.g., `test_api_requests.py`). You can run your tests by executing:
```bash
pytest test_api_requests.py
```

<<<<<<< Agents
You would run these tests using the command `pytest <test_file.py>` in your terminal. If everything is set up correctly and you have `pytest` and `mock` available in your environment, these tests should execute as intended.
=======
This should output the results of your tests, and since they operate on mock data, they will run quickly and deterministically without external dependencies.
>>>>>>> main
