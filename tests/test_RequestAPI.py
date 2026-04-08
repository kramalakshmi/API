To generate unit tests using pytest for the provided Python code, we'll utilize the `pytest` framework along with the `unittest.mock` library to mock the `requests` library's HTTP calls. This way, we can control the behavior of the HTTP responses and test our functions without actually making network requests.

Here are the unit tests for the functions defined in the original code:

```python
import pytest
from unittest.mock import patch, Mock
import requests
from my_module import get_request, post_request, put_request, delete_request

# Test case for the GET request
@patch('requests.get')
def test_get_request(mock_get):
    # Mock the response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"id": 1, "name": "John Doe"}]
    mock_get.return_value = mock_response

    get_request()  # Call the function that uses requests.get
    mock_get.assert_called_once()  # Ensure requests.get was called once

# Test case for the POST request
@patch('requests.post')
def test_post_request(mock_post):
    mock_response = Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"id": 1, "name": "Naveena"}
    mock_post.return_value = mock_response

    user_id = post_request()  # Call the function
    assert user_id == 1  # Check if the returned user ID is correct
    mock_post.assert_called_once()  # Ensure requests.post was called once

# Test case for the PUT request
@patch('requests.put')
def test_put_request(mock_put):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "name": "Naveena", "status": "inactive"}
    mock_put.return_value = mock_response

    put_request(1)  # Call the function with a test user ID
    mock_put.assert_called_once_with("https://gorest.co.in/public/v2/users/1", 
                                       json={"name": "Naveena", "email": "naveena@aa.com", "gender": "male", "status": "inactive"}, 
                                       headers={"Authorization": "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"})

# Test case for the DELETE request
@patch('requests.delete')
def test_delete_request(mock_delete):
    mock_response = Mock()
    mock_response.status_code = 204
    mock_delete.return_value = mock_response

    delete_request(1)  # Call the function with a test user ID
    mock_delete.assert_called_once_with("https://gorest.co.in/public/v2/users/1",
                                         headers={"Authorization": "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"})

# Running the tests when the script is called directly
if __name__ == "__main__":
    pytest.main()
```

### Explanation:

1. **Imports**: We're importing the necessary modules, including `pytest` for testing, `unittest.mock` for mocking HTTP requests, and the functions from the intended module (assumed to be `my_module`).

2. **Mocking Requests**: Using `@patch` decorators, we mock the `requests.get`, `requests.post`, `requests.put`, and `requests.delete` functions so we can assert that they were called correctly without making actual HTTP requests.

3. **Assertions**: Each test checks that the appropriate function was called (like `requests.get` or `requests.post`) and verifies that the returned user ID, if applicable, matches expected values.

4. **Run Tests**: At the bottom, we ensure that tests can be run directly from the script.

Make sure to replace `my_module` with the actual name of the module where your functions are defined. This testing approach ensures that you can run these tests deterministically without relying on external services.