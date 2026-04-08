To create unit tests for the provided Python code using `pytest`, we need to mock the `requests` library since the functions perform actual HTTP requests. We can use the `pytest` library alongside `unittest.mock` to create these tests.

Below are the unit tests for the code:

```python
import pytest
from unittest.mock import patch, Mock
from your_module import get_request, post_request, put_request, delete_request  # replace 'your_module' with the actual module name

class TestAPIRequests:
    
    @patch('your_module.requests.get')
    def test_get_request_success(self, mock_get):
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": 1, "name": "John Doe", "email": "john@example.com"}]
        mock_get.return_value = mock_response
        
        # Act
        get_request()
        
        # Assert
        mock_get.assert_called_once()
    
    @patch('your_module.requests.post')
    def test_post_request_success(self, mock_post):
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"id": 123, "name": "Naveena"}
        mock_post.return_value = mock_response
        
        # Act
        user_id = post_request()
        
        # Assert
        mock_post.assert_called_once()
        assert user_id == 123
    
    @patch('your_module.requests.put')
    def test_put_request_success(self, mock_put):
        # Arrange
        user_id = 123
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": user_id, "status": "inactive"}
        mock_put.return_value = mock_response
        
        # Act
        put_request(user_id)
        
        # Assert
        mock_put.assert_called_once_with(f"https://gorest.co.in/public/v2/users/{user_id}", json={
            "name": "Naveena",
            "email": "naveena@aa.com",
            "gender": "male",
            "status": "inactive"
        }, headers={"Authorization": "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"})

    @patch('your_module.requests.delete')
    def test_delete_request_success(self, mock_delete):
        # Arrange
        user_id = 123
        mock_response = Mock()
        mock_response.status_code = 204
        mock_delete.return_value = mock_response
        
        # Act
        delete_request(user_id)
        
        # Assert
        mock_delete.assert_called_once_with(f"https://gorest.co.in/public/v2/users/{user_id}", headers={"Authorization": "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"})
```

### Explanation of the Test Code:
1. **Mocking the Requests Library**: We use `unittest.mock.patch` to replace the `requests.get`, `requests.post`, `requests.put`, and `requests.delete` methods with mock objects. This avoids making actual network requests during the tests.

2. **Setup for Each Test**: Each test method sets up a mock response for the corresponding HTTP method, defining the `status_code` and returning a specific JSON response.

3. **Acting on the Functions**: Each test calls the corresponding function — `get_request`, `post_request`, etc.

4. **Assertions**: Each test asserts that the mocked HTTP method was called with the expected parameters. The tests for `post_request` and `put_request` also check that the return value is as expected.

5. **Deterministic Behavior**: The tests use fixed responses and IDs for predictable behavior, ensuring that the results won't change with environment states or external API responses.

### Note:
Remember to replace `your_module` in the import statement with the actual name of the module where your original functions are defined. Additionally, ensure that you have `pytest` and `pytest-mock` installed in your environment to run these tests.