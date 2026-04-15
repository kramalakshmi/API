import pytest
from unittest.mock import Mock, patch

from src.api_module import BASE_URL, create_post, delete_post, get_user, update_post


def test_get_user_success():
    expected = {"id": 1, "name": "Leanne Graham"}
    response = Mock(status_code=200)
    response.json.return_value = expected

    with patch("src.api_module.requests.get", return_value=response) as mock_get:
        result = get_user(1)

    mock_get.assert_called_once_with(f"{BASE_URL}/users/1")
    assert result == expected


def test_get_user_failure_raises_exception():
    response = Mock(status_code=404)

    with patch("src.api_module.requests.get", return_value=response) as mock_get:
        with pytest.raises(Exception, match="Failed to fetch user"):
            get_user(999)

    mock_get.assert_called_once_with(f"{BASE_URL}/users/999")


def test_create_post_success():
    expected = {"id": 101, "userId": 1, "title": "Test Title", "body": "Test Body"}
    response = Mock(status_code=201)
    response.json.return_value = expected

    with patch("src.api_module.requests.post", return_value=response) as mock_post:
        result = create_post(1, "Test Title", "Test Body")

    mock_post.assert_called_once_with(
        f"{BASE_URL}/posts",
        json={"userId": 1, "title": "Test Title", "body": "Test Body"},
    )
    assert result == expected


def test_create_post_failure_raises_exception():
    response = Mock(status_code=400)

    with patch("src.api_module.requests.post", return_value=response) as mock_post:
        with pytest.raises(Exception, match="Failed to create post"):
            create_post(1, "Bad Title", "Bad Body")

    mock_post.assert_called_once_with(
        f"{BASE_URL}/posts",
        json={"userId": 1, "title": "Bad Title", "body": "Bad Body"},
    )


def test_update_post_success():
    expected = {"id": 5, "title": "Updated Title", "body": "Updated Body"}
    response = Mock(status_code=200)
    response.json.return_value = expected

    with patch("src.api_module.requests.put", return_value=response) as mock_put:
        result = update_post(5, "Updated Title", "Updated Body")

    mock_put.assert_called_once_with(
        f"{BASE_URL}/posts/5",
        json={"title": "Updated Title", "body": "Updated Body"},
    )
    assert result == expected


def test_update_post_failure_raises_exception():
    response = Mock(status_code=500)

    with patch("src.api_module.requests.put", return_value=response) as mock_put:
        with pytest.raises(Exception, match="Failed to update post"):
            update_post(5, "Updated Title", "Updated Body")

    mock_put.assert_called_once_with(
        f"{BASE_URL}/posts/5",
        json={"title": "Updated Title", "body": "Updated Body"},
    )


def test_delete_post_success():
    response = Mock(status_code=200)

    with patch("src.api_module.requests.delete", return_value=response) as mock_delete:
        result = delete_post(7)

    mock_delete.assert_called_once_with(f"{BASE_URL}/posts/7")
    assert result is True


def test_delete_post_failure_raises_exception():
    response = Mock(status_code=404)

    with patch("src.api_module.requests.delete", return_value=response) as mock_delete:
        with pytest.raises(Exception, match="Failed to delete post"):
            delete_post(7)

    mock_delete.assert_called_once_with(f"{BASE_URL}/posts/7")
