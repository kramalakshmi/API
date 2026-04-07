To create unit tests for the provided Python code using `pytest`, we need to mock the external HTTP requests made using the `requests` library. This allows us to test the functionality without actually making calls to the external API, ensuring our tests are deterministic.

Here is an example of how to structure your tests using `pytest` and the `unittest.mock` module:

```python
import pytest
from unittest.mock import patch, Mock
import requests
from your_module import get_request, post_request, put_request, delete_request  # Adjust the import statement

@pytest.fixture
def mock_requests():
    with patch('requests.get') as mock_get, \
         patch('requests.post') as mock_post, \
         patch('requests.put') as mock_put, \
         patch('requests.delete') as mock_delete:
        yield mock_get, mock_post, mock_put, mock_delete

def test_get_request(mock_requests):
    mock_get, _, _, _ = mock_requests
    mock_get.return_value = Mock(status_code=200, json=lambda: [{"id": 1, "name": "Test User"}])
    
    get_request()  # Call the function
    
    mock_get.assert_called_once()  # Ensure GET request was made

def test_post_request(mock_requests):
    mock_get, mock_post, _, _ = mock_requests
    mock_post.return_value = Mock(status_code=201, json=lambda: {"id": 1})

    user_id = post_request()  # Call the function
    
    assert user_id == 1  # Check if the returned user ID is correct
    mock_post.assert_called_once()  # Ensure POST request was made

def test_put_request(mock_requests):
    mock_get, mock_post, mock_put, _ = mock_requests
    mock_put.return_value = Mock(status_code=200, json=lambda: {"id": 1})

    put_request(1)  # Call the function
    
    mock_put.assert_called_once_with(
        'https://gorest.co.in/public/v2/users/1',
        json={
            "name": "Naveena",
            "email": "naveena@aa.com",
            "gender": "male",
            "status": "inactive"
        },
        headers={"Authorization": "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"}
    )  # Ensure PUT request was made with the correct parameters

def test_delete_request(mock_requests):
    mock_get, mock_post, mock_put, mock_delete = mock_requests
    mock_delete.return_value = Mock(status_code=204)

    delete_request(1)  # Call the function

    mock_delete.assert_called_once_with('https://gorest.co.in/public/v2/users/1', 
                                         headers={"Authorization": "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"})  # Assert DELETE request was made

if __name__ == "__main__":
    pytest.main()
```

### Breakdown of the tests:

1. **Mocking**: We use `unittest.mock.patch` to mock the `requests.get`, `requests.post`, `requests.put`, and `requests.delete` methods so we don't make actual API calls.

2. **Fixtures**: The `mock_requests` fixture sets up the mocked functions and is used in each test to ensure we are not repeating code.

3. **Testing Response**: Each test checks if the function correctly calls the appropriate HTTP method and verifies the returned values where applicable.

4. **Adjust the Import Statement**: Replace `your_module` with the actual name of the Python file or module where your original code resides.

5. **Running Tests**: The `if __name__ == "__main__":` block with `pytest.main()` allows running the tests directly if the file is executed.

This setup provides clear, isolated tests for each function that test the expected outcomes without relying on the external API.