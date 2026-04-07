To create unit tests for the provided Python code, we can use the `pytest` framework along with the `unittest.mock` library to mock the HTTP requests made by the `requests` library. This way, we can create predictable and repeatable tests without actually hitting the external API.

Here are the test cases for the `get_request`, `post_request`, `put_request`, and `delete_request` functions:

```python
import pytest
from unittest.mock import patch, Mock
import requests
from your_module import get_request, post_request, put_request, delete_request  # replace "your_module" with the actual module name


class TestAPIRequests:
    @patch('requests.get')
    def test_get_request_success(self, mock_get):
        # Set up the mock to return a successful response
        mock_get.return_value = Mock(status_code=200, json=lambda: [{"id": 1, "name": "Test User"}])
        
        get_request()
        
        # Assert the mock was called with the correct URL
        mock_get.assert_called_once_with('https://gorest.co.in/public/v2/users', headers={'Authorization': 'Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405'})

    @patch('requests.post')
    def test_post_request_success(self, mock_post):
        # Set up the mock to return a successful response
        mock_post.return_value = Mock(status_code=201, json=lambda: {"id": 123, "name": "Test User"})
        
        user_id = post_request()
        
        # Assert the mock was called with the correct URL and data
        mock_post.assert_called_once_with('https://gorest.co.in/public/v2/users', json={
            "name": "Naveena",
            "email": "naveean@aa.com",
            "gender": "male",
            "status": "active"
        }, headers={'Authorization': 'Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405'})
        
        # Assert the returned user_id is as expected
        assert user_id == 123

    @patch('requests.put')
    def test_put_request_success(self, mock_put):
        user_id = 123
        # Set up the mock to return a successful response
        mock_put.return_value = Mock(status_code=200, json=lambda: {"id": user_id, "name": "Updated User"})
        
        put_request(user_id)
        
        # Assert the mock was called with the correct URL and data
        mock_put.assert_called_once_with(f'https://gorest.co.in/public/v2/users/{user_id}', json={
            "name": "Naveena",
            "email": "naveena@aa.com",
            "gender": "male",
            "status": "inactive"
        }, headers={'Authorization': 'Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405'})

    @patch('requests.delete')
    def test_delete_request_success(self, mock_delete):
        user_id = 123
        # Set up the mock to return a successful response for delete
        mock_delete.return_value = Mock(status_code=204)
        
        delete_request(user_id)
        
        # Assert the mock was called with the correct URL
        mock_delete.assert_called_once_with(f'https://gorest.co.in/public/v2/users/{user_id}', headers={'Authorization': 'Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405'})
```

### Explanation:

1. **Mocking HTTP Calls**: Each test method uses `@patch` to replace the `requests.get`, `requests.post`, `requests.put`, or `requests.delete` method with a mock object. This prevents actual HTTP requests during testing.

2. **Setting Up Mocks**: Each test case sets up the mock to return a predefined status code and JSON response that the function under test expects. For example, the `post_request` test returns a JSON object containing an `id` that the `post_request` function will return.

3. **Assertions**: After the function call, we assert:
   - That the mock was called with the correct URL and parameters.
   - For the `post_request`, we also assert the returned value (user ID) matches the expected result.

To run the tests, you will need to place the test code in a file and execute it using `pytest`, typically with a command like `pytest test_your_module.py` in your terminal. Make sure to replace `your_module` with the name of the module where your original code resides.