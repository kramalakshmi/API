import pytest
from unittest.mock import patch
from your_module import get_data, post_data, put_data  # Adjust the import according to your module name

# Sample responses to mock for the tests
mock_get_response = {"userId": 1, "id": 1, "title": "Test title", "body": "Test body"}
mock_post_response = {"id": 101, "title": "Test"}
mock_put_response = {"id": 1, "title": "Updated"}

# Test for the get_data function
@patch('requests.get')
def test_get_data(mock_get):
    mock_get.return_value.json.return_value = mock_get_response
    url = "https://jsonplaceholder.typicode.com/posts/1"
    response = get_data(url)
    assert response == mock_get_response
    mock_get.assert_called_once_with(url)

# Test for the post_data function
@patch('requests.post')
def test_post_data(mock_post):
    mock_post.return_value.json.return_value = mock_post_response
    url = "https://jsonplaceholder.typicode.com/posts"
    payload = {"title": "Test"}
    response = post_data(url, payload)
    assert response == mock_post_response
    mock_post.assert_called_once_with(url, json=payload)

# Test for the put_data function
@patch('requests.put')
def test_put_data(mock_put):
    mock_put.return_value.json.return_value = mock_put_response
    url = "https://jsonplaceholder.typicode.com/posts/1"
    payload = {"title": "Updated"}
    response = put_data(url, payload)
    assert response == mock_put_response
    mock_put.assert_called_once_with(url, json=payload)

if __name__ == "__main__":
    pytest.main()
```

### Explanation
1. **Mocking**: We use `@patch` to mock the `requests.get`, `requests.post`, and `requests.put` functions so that our tests do not make actual HTTP requests.

2. **Controlled Responses**: We define sample responses for each type of request, which are returned when the mocked methods are called.

3. **Assertions**: Each test verifies that the function correctly processes the response and that the requests are called with the expected parameters.

4. **Deterministic Input**: The test cases use fixed URLs and payloads, making them predictable and repeatable.

5. **Running Tests**: The bottom line allows you to run the tests if this script is executed directly. 

Make sure to replace `your_module` with the appropriate module name where the functions are defined.
