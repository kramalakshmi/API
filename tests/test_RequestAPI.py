To generate unit tests for the provided Python code using `pytest`, we will use the `unittest.mock` module to mock the `requests` library. This allows us to simulate the behavior of the HTTP requests without actually making calls to the external API. This method makes our tests deterministic and ensures they can run quickly without network dependency.

Here's how you might write the tests in a separate file, such as `test_api_requests.py`:

```python
import pytest
from unittest.mock import patch, Mock
import requests
from your_module import get_request, post_request, put_request, delete_request  # Replace 'your_module' with the actual module name where the functions are defined.

# To structure and reuse the responses for tests
class MockResponse:
    @staticmethod
    def json():
        return {"id": 1234}  # Example response for POST request

    @property
    def status_code(self):
        return 200  # Default status code


def test_get_request():
    with patch('requests.get') as mocked_get:
        mocked_get.return_value = MockResponse()  # Mock response
        get_request()
        mocked_get.assert_called_once()  # Ensure the GET request is called once


def test_post_request():
    with patch('requests.post') as mocked_post:
        # Setup mock response
        mocked_post.return_value = MockResponse()
        user_id = post_request()
        
        assert user_id == 1234  # Verify the returned user_id
        mocked_post.assert_called_once()  # Ensure the POST request is called once


def test_put_request():
    user_id = 1234
    with patch('requests.put') as mocked_put:
        mocked_put.return_value = MockResponse()  # Mock PUT response
        put_request(user_id)
        mocked_put.assert_called_once_with(
            f"https://gorest.co.in/public/v2/users/{user_id}",
            json={"name": "Naveena", "email": "naveena@aa.com", "gender": "male", "status": "inactive"},
            headers={"Authorization": "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"},
        )  # Ensure the PUT request is called once and with correct arguments


def test_delete_request():
    user_id = 1234
    with patch('requests.delete') as mocked_delete:
        mocked_delete.return_value = MockResponse()  # Mock DELETE response
        delete_request(user_id)
        mocked_delete.assert_called_once_with(
            f"https://gorest.co.in/public/v2/users/{user_id}",
            headers={"Authorization": "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"}
        )  # Ensure the DELETE request is called once and with correct arguments


# The following is to be called if you're running the tests using pytest directly
if __name__ == "__main__":
    pytest.main()
```

### Explanation:
1. **MockResponse Class**: Simulates the behavior of a typical HTTP response for our tests, providing a `json()` method and a `status_code` property.
  
2. **Test Functions**:
   - Each function uses `patch` from `unittest.mock` to replace the `requests` methods (`get`, `post`, `put`, `delete`) with a mock object for that test's scope.
   - Assertions are made to ensure that the methods are called correctly and return expected results.
   - The `user_id` is hardcoded in the mocks and assertions to keep the tests deterministic.

3. **Running Tests**: The last line allows running the tests from the command line.

Make sure to replace `'your_module'` with the actual name of your Python file (without the `.py` extension) whenever you're importing the functions to test. 

With this setup, your unit tests are clear, deterministic, and do not rely on external network calls, making them robust and quick to execute.