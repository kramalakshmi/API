To test the provided Python code, we will create a set of unit tests using the `pytest` framework. Since the functions make actual HTTP requests using the `requests` library, we will use the `pytest-mock` library to mock the responses of these requests.

Here's how you can write deterministic tests for the `get_data`, `post_data`, and `put_data` functions using `pytest`.

```python
import pytest
import requests
from unittest.mock import patch

# Assuming the functions get_data, post_data, and put_data are imported from the module where they are defined.
from your_module import get_data, post_data, put_data  # Replace 'your_module' with the actual module name


def test_get_data():
    url = "https://jsonplaceholder.typicode.com/posts/1"
    expected_response = {
        "userId": 1,
        "id": 1,
        "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
        "body": "quia et suscipit\nsuscipit ..."
    }

    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = expected_response
        response = get_data(url)
        
        mock_get.assert_called_once_with(url)
        assert response == expected_response


def test_post_data():
    url = "https://jsonplaceholder.typicode.com/posts"
    payload = {"title": "Test"}
    expected_response = {"id": 101, "title": "Test"}

    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = expected_response
        response = post_data(url, payload)
        
        mock_post.assert_called_once_with(url, json=payload)
        assert response == expected_response


def test_put_data():
    url = "https://jsonplaceholder.typicode.com/posts/1"
    payload = {"title": "Updated"}
    expected_response = {"id": 1, "title": "Updated"}

    with patch('requests.put') as mock_put:
        mock_put.return_value.json.return_value = expected_response
        response = put_data(url, payload)
        
        mock_put.assert_called_once_with(url, json=payload)
        assert response == expected_response


if __name__ == "__main__":
    pytest.main()
```

### Explanation
1. **Imports**: We import `pytest` for the testing framework and `patch` from `unittest.mock` to mock HTTP requests.

2. **Mocking External Calls**: The `patch` function is used to mock `requests.get`, `requests.post`, and `requests.put`. This means that the actual network calls are not made, and instead, we provide our expectations for the return values.

3. **Deterministic Test Cases**: We define expected return values for each function (e.g., the expected JSON response structure). The tests ensure that the mocked function is called with the expected arguments and returns the expected result.

4. **Assertions**: The tests include assertions to verify that:
   - The request function was called with the correct URL and data (for POST and PUT).
   - The returned data matches the expected response. 

### Running the Tests
You can run these tests by saving the test code in a file (e.g., `test_your_module.py`) and executing `pytest test_your_module.py` in your terminal. Make sure `pytest` and `pytest-mock` are installed in your environment.