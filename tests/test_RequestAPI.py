To write unit tests using `pytest` for the code you provided, you need to mock the HTTP requests made by the `requests` library. This way, you can simulate different server responses without actually hitting the external API.

First, you'll want to install the required library for mocking if you haven't done so:

```bash
pip install pytest pytest-mock
```

Here’s a potential structure for the test suite using `pytest` and `unittest.mock`:

```python
import pytest
import requests
from unittest.mock import patch

# Assuming the provided code is in a module named `api_requests`
# from api_requests import get_request, post_request, put_request, delete_request

# You can use patch to mock requests.get, requests.post, requests.put, requests.delete
class TestApiRequests:

    @patch('requests.get')
    def test_get_request_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"id": 1, "name": "John Doe"}]
        
        # Assuming there's a print capturing mechanism here.
        get_request()  # Here it won't return anything, you might want to modify it to return the response

        assert mock_get.called
        assert mock_get.call_count == 1

    @patch('requests.post')
    def test_post_request_success(self, mock_post):
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {"id": 123, "name": "Naveena"}
        
        user_id = post_request()
        
        assert user_id == 123
        assert mock_post.called
        assert mock_post.call_count == 1

    @patch('requests.put')
    def test_put_request_success(self, mock_put):
        mock_put.return_value.status_code = 200
        mock_put.return_value.json.return_value = {"id": 123, "name": "Naveena", "status": "inactive"}
        
        put_request(123)  # Assume user_id 123
        
        assert mock_put.called
        assert mock_put.call_count == 1

    @patch('requests.delete')
    def test_delete_request_success(self, mock_delete):
        mock_delete.return_value.status_code = 204
        
        delete_request(123)  # Assume user_id 123
        
        assert mock_delete.called
        assert mock_delete.call_count == 1

# Run the tests with: pytest -v
```

### Explanation of the Test Cases:

1. **test_get_request_success**: 
   - This test mocks a successful `GET` request with a 200 status code. You can check whether the `get_request` function is called once and confirm the expected behavior.

2. **test_post_request_success**: 
   - This test mocks a successful `POST` request, simulating the creation of a user. You check that the returned user_id matches the mock response.

3. **test_put_request_success**: 
   - This test mocks a successful `PUT` request updating a user's information. It ensures that the function executes the request correctly.

4. **test_delete_request_success**: 
   - This test mocks a successful `DELETE` request and verifies that the function was called correctly.

*Remember to replace the comment about the import with the actual module name that contains the requests code you provided.*

By running these tests, you can effectively validate the functionality of the code without needing access to a live API, ensuring the tests are deterministic and repeatable.