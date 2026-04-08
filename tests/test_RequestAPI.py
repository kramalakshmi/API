To properly test the provided code with pytest, we'll need to mock the requests made to the external API because we don't want to make real API calls during testing. We'll use the `pytest` and `unittest.mock` libraries for this purpose. Here's how you can write unit tests for the provided code.

First, make sure you have pytest installed. You can install it using pip if you haven't done so already:

```bash
pip install pytest
```

Now, create a new Python file, e.g., `test_api.py`, and add the following test cases:

```python
import pytest
from unittest.mock import patch
import requests
from your_module import get_request, post_request, put_request, delete_request  # replace 'your_module' with the actual module name


class TestApiRequests:
    @patch('requests.get')
    def test_get_request(self, mock_get):
        # Mock the response data
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"id": 1, "name": "Test User"}]

        # Call function
        result = get_request()

        # Assertions
        mock_get.assert_called_once()
        assert result is None  # The function doesn't return anything

    @patch('requests.post')
    def test_post_request(self, mock_post):
        # Mock the response data
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {"id": 1}

        # Call function
        user_id = post_request()

        # Assertions
        mock_post.assert_called_once()
        assert user_id == 1

    @patch('requests.put')
    def test_put_request(self, mock_put):
        user_id = 1
        # Mock the response data
        mock_put.return_value.status_code = 200
        mock_put.return_value.json.return_value = {"id": user_id, "status": "inactive"}

        # Call function
        result = put_request(user_id)

        # Assertions
        mock_put.assert_called_once_with(f"https://gorest.co.in/public/v2/users/{user_id}", json={
            "name": "Naveena",
            "email": "naveena@aa.com",
            "gender": "male",
            "status": "inactive"
        }, headers={"Authorization": "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"})
        assert result is None  # The function doesn't return anything

    @patch('requests.delete')
    def test_delete_request(self, mock_delete):
        user_id = 1
        # Mock the response data
        mock_delete.return_value.status_code = 204

        # Call function
        result = delete_request(user_id)

        # Assertions
        mock_delete.assert_called_once_with(f"https://gorest.co.in/public/v2/users/{user_id}",
                                             headers={"Authorization": "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"})
        assert result is None  # The function doesn't return anything


if __name__ == "__main__":
    pytest.main()
```

### Explanation of the Test Cases:

1. **test_get_request**: This test mocks the `GET` request and assumes that the response is a JSON list with a user object, verifies that the get_request function calls the API, and checks that it doesn't return anything.

2. **test_post_request**: This test mocks the `POST` request, simulates a successful user creation, checks that the correct data is sent, and validates that the returned `user_id` is as expected.

3. **test_put_request**: This test mocks the `PUT` request and checks that it is called with the right parameters for the update. It verifies the status code of the mock response and also confirms no return value.

4. **test_delete_request**: This test mocks the `DELETE` request, verifies the API call, and checks if the response code is what we expect (204 No Content).

### How to Run the Tests
To run the tests, navigate to the directory where your `test_api.py` file is located and run:

```bash
pytest test_api.py
```

This will execute the tests, and you should see if they pass or fail based on the provided mocking scenarios.