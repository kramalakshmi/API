To create unit tests for the provided Python code, we can use the `pytest` framework along with `unittest.mock` to mock the HTTP requests made by the `requests` library. This ensures that our tests are deterministic and do not rely on actual API calls. Below are example unit tests for the defined functions:

```python
import pytest
from unittest.mock import patch, Mock
import requests

# Assuming the provided code is in a file named `api_client.py`
from api_client import get_request, post_request, put_request, delete_request


class TestApiClient:
    
    @patch('requests.get')
    def test_get_request_success(self, mock_get):
        # Mocking the response from the GET request
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": 1, "name": "User1"}, {"id": 2, "name": "User2"}]
        mock_get.return_value = mock_response

        get_request()  # Call the function

        # Assert that the GET request was made once
        mock_get.assert_called_once()
    
    @patch('requests.post')
    def test_post_request_success(self, mock_post):
        # Mocking the response from the POST request
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"id": 123}
        mock_post.return_value = mock_response

        user_id = post_request()  # Call the function
        
        # Assert that the POST request was made once
        mock_post.assert_called_once()
        # Assert that the returned user_id is as expected
        assert user_id == 123

    @patch('requests.put')
    def test_put_request_success(self, mock_put):
        # Mocking the response from the PUT request
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 123, "name": "Updated User"}
        mock_put.return_value = mock_response
        
        user_id = 123  # Example user ID for testing
        put_request(user_id)  # Call the function
        
        # Assert that the PUT request was made once with the correct URL
        mock_put.assert_called_once_with(
            f'https://gorest.co.in/public/v2/users/{user_id}', 
            json={
                "name": "Naveena",
                "email": "naveena@aa.com",
                "gender": "male",
                "status": "inactive"
            },
            headers={"Authorization": "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"}
        )

    @patch('requests.delete')
    def test_delete_request_success(self, mock_delete):
        # Mocking the response from the DELETE request
        mock_response = Mock()
        mock_response.status_code = 204
        mock_delete.return_value = mock_response
        
        user_id = 123  # Example user ID for testing
        delete_request(user_id)  # Call the function
        
        # Assert that the DELETE request was made once with the correct URL
        mock_delete.assert_called_once_with(f'https://gorest.co.in/public/v2/users/{user_id}', 
                                             headers={"Authorization": "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"})
```

### Explanation:
1. **Mocks**: We use `unittest.mock.patch` to replace `requests.get`, `requests.post`, `requests.put`, and `requests.delete` with mock objects. This allows us to simulate their responses.

2. **Testing GET Request**: We mock a successful GET request response to test that `get_request` is functioning as expected with proper assertions on calls.

3. **Testing POST Request**: Similarly, we mock a POST request to check if the `post_request` function behaves correctly, asserting that it returns the expected user ID.

4. **Testing PUT Request**: We mock the PUT request and assert that it is called with the expected arguments.

5. **Testing DELETE Request**: We mock the DELETE request and ensure it is called correctly.

### Usage:
To run the tests, save the test code in a file (e.g., `test_api_client.py`) and run it using `pytest`.
```bash
pytest test_api_client.py
``` 

You would run these tests using the command `pytest <test_file.py>` in your terminal. If everything is set up correctly and you have `pytest` and `mock` available in your environment, these tests should execute as intended.
