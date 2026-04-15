import pytest
from unittest.mock import Mock, patch

from src.api_module import BASE_URL, create_post, delete_post, get_user, update_post


def test_get_user_success():
    user_id = 1
    expected = {"id": user_id, "name": "Leanne Graham"}
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = expected

    with patch("src.api_module.requests.get", return_value=mock_response) as mock_get:
        result = get_user(user_id)

    mock_get.assert_called_once_with(f"{BASE_URL}/users/{user_id}")
    assert result == expected


def test_get_user_failure_raises_exception():
    mock_response = Mock(status_code=404)

    with patch("src.api_module.requests.get", return_value=mock_response) as mock_get:
        with pytest.raises(Exception, match="Failed to fetch user"):
            get_user(999)

    mock_get.assert_called_once_with(f"{BASE_URL}/users/999")


def test_create_post_success():
    user_id = 2
    title = "Test Title"
    body = "Test Body"
    expected = {"id": 101, "userId": user_id, "title": title, "body": body}
    mock_response = Mock(status_code=201)
    mock_response.json.return_value = expected

    with patch("src.api_module.requests.post", return_value=mock_response) as mock_post:
        result = create_post(user_id, title, body)

    mock_post.assert_called_once_with(
        f"{BASE_URL}/posts",
        json={"userId": user_id, "title": title, "body": body},
    )
    assert result == expected


def test_create_post_failure_raises_exception():
    user_id = 2
    title = "Bad Title"
    body = "Bad Body"
    mock_response = Mock(status_code=400)

    with patch("src.api_module.requests.post", return_value=mock_response) as mock_post:
        with pytest.raises(Exception, match="Failed to create post"):
            create_post(user_id, title, body)

    mock_post.assert_called_once_with(
        f"{BASE_URL}/posts",
        json={"userId": user_id, "title": title, "body": body},
    )


def test_update_post_success():
    post_id = 5
    title = "Updated Title"
    body = "Updated Body"
    expected = {"id": post_id, "title": title, "body": body}
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = expected

    with patch("src.api_module.requests.put", return_value=mock_response) as mock_put:
        result = update_post(post_id, title, body)

    mock_put.assert_called_once_with(
        f"{BASE_URL}/posts/{post_id}",
        json={"title": title, "body": body},
    )
    assert result == expected


def test_update_post_failure_raises_exception():
    post_id = 5
    title = "Updated Title"
    body = "Updated Body"
    mock_response = Mock(status_code=500)

    with patch("src.api_module.requests.put", return_value=mock_response) as mock_put:
        with pytest.raises(Exception, match="Failed to update post"):
            update_post(post_id, title, body)

    mock_put.assert_called_once_with(
        f"{BASE_URL}/posts/{post_id}",
        json={"title": title, "body": body},
    )


def test_delete_post_success():
    post_id = 10
    mock_response = Mock(status_code=200)

    with patch("src.api_module.requests.delete", return_value=mock_response) as mock_delete:
        result = delete_post(post_id)

    mock_delete.assert_called_once_with(f"{BASE_URL}/posts/{post_id}")
    assert result is True


def test_delete_post_failure_raises_exception():
    post_id = 10
    mock_response = Mock(status_code=404)

    with patch("src.api_module.requests.delete", return_value=mock_response) as mock_delete:
        with pytest.raises(Exception, match="Failed to delete post"):
            delete_post(post_id)

    mock_delete.assert_called_once_with(f"{BASE_URL}/posts/{post_id}")
