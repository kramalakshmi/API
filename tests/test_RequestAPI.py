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
 

