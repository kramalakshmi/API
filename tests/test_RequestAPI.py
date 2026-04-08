To test the provided Python code using `pytest`, we will want to use the `requests` library's capabilities to mock HTTP requests and responses. We'll create unit tests for each of the HTTP methods (GET, POST, PUT, DELETE) to ensure they behave as expected.

Here are the unit tests:

```python
import pytest
import requests
from unittest import mock

# Assuming the above code is in a module named `api_module`
from api_module import get_request, post_request, put_request, delete_request

@pytest.fixture
def mock_requests():
    with mock.patch('api_module.requests') as mock_requests:
        yield mock_requests

def test_get_request(mock_requests):
    """ Tests the get_request function. """
    # Mocking the response
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"id": 1, "name": "John"}]  # Sample user data
    mock_requests.get.return_value = mock_response
    
    get_request()
    
    # Assert that the requests.get was called with the expected URL and headers
    mock_requests.get.assert_called_once_with("https://gorest.co.in/public/v2/users", 
                                               headers={"Authorization": "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"})

def test_post_request(mock_requests):
    """ Tests the post_request function. """
    # Mocking the response
    mock_response = mock.Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"id": 2, "name": "Naveena"}  # Simulated return data
    mock_requests.post.return_value = mock_response
    
    user_id = post_request()
    
    # Assert that user_id is correctly returned
    assert user_id == 2
    # Assert that the requests.post was called with the expected URL, data and headers
    mock_requests.post.assert_called_once_with("https://gorest.co.in/public/v2/users", 
                                                json={"name": "Naveena", "email": "naveean@aa.com", "gender": "male", "status": "active"}, 
                                                headers={"Authorization": "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"})

def test_put_request(mock_requests):
    """ Tests the put_request function. """
    user_id = 3  # Example user ID
    # Mocking the response
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": user_id, "name": "Naveena", "status": "inactive"}  # Sample response
    mock_requests.put.return_value = mock_response
    
    put_request(user_id)
    
    # Assert that the requests.put was called with the expected URL, data, and headers
    mock_requests.put.assert_called_once_with("https://gorest.co.in/public/v2/users/3", 
                                               json={"name": "Naveena", "email": "naveena@aa.com", "gender": "male", "status": "inactive"}, 
                                               headers={"Authorization": "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"})

def test_delete_request(mock_requests):
    """ Tests the delete_request function. """
    user_id = 4  # Example user ID
    # Mocking the response
    mock_response = mock.Mock()
    mock_response.status_code = 204
    mock_requests.delete.return_value = mock_response
    
    delete_request(user_id)
    
    # Assert that the requests.delete was called with the expected URL and headers
    mock_requests.delete.assert_called_once_with("https://gorest.co.in/public/v2/users/4", 
                                                  headers={"Authorization": "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"})

if __name__ == "__main__":
    pytest.main()
```

### Explanation:
1. **Mocking Requests**: We leverage `unittest.mock.patch` to mock the `requests` module used in your API functions. This prevents actual API calls during the tests, enabling us to create deterministic responses.

2. **Test Functions**: Each test function corresponds to an API method:
   - `test_get_request`: Tests the `get_request` function with a mock response.
   - `test_post_request`: Tests the `post_request` function, checks if it returns the correct user ID.
   - `test_put_request`: Tests the `put_request` function with a user ID.
   - `test_delete_request`: Tests the `delete_request` function with a user ID.

3. **Assertions**: We assert that the mocked requests were called with the expected URLs, data, and headers. This verifies that our functions work correctly with the requests module.

4. **Using Fixtures**: The `mock_requests` fixture is used to provide a mock version of the `requests` module to each test. 

This structure keeps the tests clear, deterministic, and focused on functionality rather than network behavior. To run these tests, you should install `pytest` and run the current script where these tests are defined.