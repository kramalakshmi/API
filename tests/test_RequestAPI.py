To create unit tests using `pytest` for the given Python code, we will mock the `requests` library to avoid actual API calls. The tests will focus on checking the functionality of the `get_request`, `post_request`, `put_request`, and `delete_request` functions.

Before we proceed with the tests, ensure that the `pytest` library and `pytest-mock` are installed in your environment. You can install them via pip:

```bash
pip install pytest pytest-mock
```

Here are the unit tests:

```python
import pytest
from unittest.mock import patch
import requests
from your_module import get_request, post_request, put_request, delete_request  # Replace 'your_module' with the actual module name

class TestAPIRequests:

    @patch('requests.get')
    def test_get_request_success(self, mock_get):
        # Arrange
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"id": 1, "name": "John Doe"}]

        # Act
        get_request()

        # Assert
        mock_get.assert_called_once()

    @patch('requests.post')
    def test_post_request_success(self, mock_post):
        # Arrange
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {"id": 123, "name": "Naveena"}

        # Act
        user_id = post_request()

        # Assert
        assert user_id == 123
        mock_post.assert_called_once()

    @patch('requests.put')
    def test_put_request_success(self, mock_put):
        # Arrange
        mock_put.return_value.status_code = 200
        mock_put.return_value.json.return_value = {"id": 123, "name": "Naveena", "status": "inactive"}

        # Act
        put_request(123)

        # Assert
        mock_put.assert_called_once_with(
            "https://gorest.co.in/public/v2/users/123",
            json={"name": "Naveena", "email": "naveena@aa.com", "gender": "male", "status": "inactive"},
            headers={"Authorization": "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"}
        )

    @patch('requests.delete')
    def test_delete_request_success(self, mock_delete):
        # Arrange
        mock_delete.return_value.status_code = 204

        # Act
        delete_request(123)

        # Assert
        mock_delete.assert_called_once_with(
            "https://gorest.co.in/public/v2/users/123",
            headers={"Authorization": "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"}
        )
```

### Explanation:

1. **Environment Setup**: Make sure you've installed `pytest` and `pytest-mock`, and replace `your_module` with the actual name of your module containing the functions.

2. **Mocking**: Each test uses `@patch` from the `unittest.mock` library to replace `requests.get`, `requests.post`, `requests.put`, and `requests.delete` with mock objects. This prevents any real HTTP requests from being sent.

3. **Testing**:
   - The `test_get_request_success` checks if the GET request is made successfully.
   - The `test_post_request_success` checks if the POST request returns the correct user ID.
   - The `test_put_request_success` verifies that the PUT request is formed correctly and that the API is called with the expected URL and payload.
   - The `test_delete_request_success` confirms that the DELETE request is called with the correct URL.

### Execute the Tests:
You can execute the tests using the following command in your command line:

```bash
pytest test_your_module.py  # Replace with your actual test file name
```

This will run the tests, and you should see the results in the console. Adjust the tests as you need based on your actual implementation and further requirements.
