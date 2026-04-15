import pytest
from unittest.mock import MagicMock, patch


def test_get_user_success():
    from src.api_module import get_user

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "name": "Alice"}

    with patch("src.api_module.requests.get", return_value=mock_response) as mock_get:
        result = get_user(1)

    mock_get.assert_called_once_with("https://jsonplaceholder.typicode.com/users/1")
    assert result == {"id": 1, "name": "Alice"}


def test_get_user_failure_raises_exception():
    from src.api_module import get_user

    mock_response = MagicMock()
    mock_response.status_code = 500

    with patch("src.api_module.requests.get", return_value=mock_response) as mock_get:
        with pytest.raises(Exception, match="Failed to fetch user"):
            get_user(1)

    mock_get.assert_called_once_with("https://jsonplaceholder.typicode.com/users/1")


def test_create_post_success():
    from src.api_module import create_post

    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"id": 101, "userId": 1, "title": "t", "body": "b"}

    with patch("src.api_module.requests.post", return_value=mock_response) as mock_post:
        result = create_post(1, "t", "b")

    mock_post.assert_called_once_with(
        "https://jsonplaceholder.typicode.com/posts",
        json={"userId": 1, "title": "t", "body": "b"},
    )
    assert result == {"id": 101, "userId": 1, "title": "t", "body": "b"}


def test_create_post_failure_raises_exception():
    from src.api_module import create_post

    mock_response = MagicMock()
    mock_response.status_code = 200

    with patch("src.api_module.requests.post", return_value=mock_response) as mock_post:
        with pytest.raises(Exception, match="Failed to create post"):
            create_post(1, "t", "b")

    mock_post.assert_called_once_with(
        "https://jsonplaceholder.typicode.com/posts",
        json={"userId": 1, "title": "t", "body": "b"},
    )


def test_update_post_success():
    from src.api_module import update_post

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "title": "t2", "body": "b2"}

    with patch("src.api_module.requests.put", return_value=mock_response) as mock_put:
        result = update_post(1, "t2", "b2")

    mock_put.assert_called_once_with(
        "https://jsonplaceholder.typicode.com/posts/1",
        json={"title": "t2", "body": "b2"},
    )
    assert result == {"id": 1, "title": "t2", "body": "b2"}


def test_update_post_failure_raises_exception():
    from src.api_module import update_post

    mock_response = MagicMock()
    mock_response.status_code = 404

    with patch("src.api_module.requests.put", return_value=mock_response) as mock_put:
        with pytest.raises(Exception, match="Failed to update post"):
            update_post(1, "t", "b")

    mock_put.assert_called_once_with(
        "https://jsonplaceholder.typicode.com/posts/1",
        json={"title": "t", "body": "b"},
    )


def test_delete_post_success():
    from src.api_module import delete_post

    mock_response = MagicMock()
    mock_response.status_code = 200

    with patch("src.api_module.requests.delete", return_value=mock_response) as mock_delete:
        result = delete_post(1)

    mock_delete.assert_called_once_with("https://jsonplaceholder.typicode.com/posts/1")
    assert result is True


def test_delete_post_failure_raises_exception():
    from src.api_module import delete_post

    mock_response = MagicMock()
    mock_response.status_code = 500

    with patch("src.api_module.requests.delete", return_value=mock_response) as mock_delete:
        with pytest.raises(Exception, match="Failed to delete post"):
            delete_post(1)

    mock_delete.assert_called_once_with("https://jsonplaceholder.typicode.com/posts/1")
