import pytest
from unittest.mock import MagicMock, patch

from src.complex_api_module import APIClient, BASE_URL


def test_init_sets_attributes_and_session():
    client = APIClient(token="tok", retries=5, timeout=9)
    assert client.token == "tok"
    assert client.retries == 5
    assert client.timeout == 9
    assert client.session is not None


def test_headers_without_token():
    client = APIClient()
    assert client._headers() == {"Accept": "application/json"}


def test_headers_with_token():
    client = APIClient(token="abc123")
    assert client._headers() == {
        "Accept": "application/json",
        "Authorization": "Bearer abc123",
    }


def test_get_user_success_without_details():
    client = APIClient(token="abc", retries=2, timeout=7)
    expected = {"id": 1, "name": "Jane"}

    with patch.object(client.session, "get") as mock_get:
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = expected
        mock_get.return_value = response

        result = client.get_user(user_id=1, include_details=False)

    assert result == expected
    mock_get.assert_called_once_with(
        f"{BASE_URL}/users/1",
        headers={"Accept": "application/json", "Authorization": "Bearer abc"},
        params={},
        timeout=7,
    )


def test_get_user_success_with_details_after_retry():
    client = APIClient(retries=2, timeout=3)

    with patch.object(client.session, "get") as mock_get, patch("src.complex_api_module.time.sleep") as mock_sleep:
        first = MagicMock()
        first.status_code = 500
        second = MagicMock()
        second.status_code = 200
        second.json.return_value = {"id": 2, "details": True}
        mock_get.side_effect = [first, second]

        result = client.get_user(user_id=2, include_details=True)

    assert result == {"id": 2, "details": True}
    assert mock_get.call_count == 2
    mock_get.assert_any_call(
        f"{BASE_URL}/users/2",
        headers={"Accept": "application/json"},
        params={"details": "1"},
        timeout=3,
    )
    mock_sleep.assert_called_once_with(0.1)


def test_get_user_raises_after_all_retries_fail():
    client = APIClient(retries=3)

    with patch.object(client.session, "get") as mock_get, patch("src.complex_api_module.time.sleep") as mock_sleep:
        response = MagicMock()
        response.status_code = 500
        mock_get.return_value = response

        with pytest.raises(Exception, match="Failed to fetch user"):
            client.get_user(user_id=1)

    assert mock_get.call_count == 3
    assert mock_sleep.call_count == 3


def test_create_user_success():
    client = APIClient(token="xyz", timeout=4)

    with patch.object(client.session, "post") as mock_post:
        response = MagicMock()
        response.status_code = 201
        response.json.return_value = {"id": 10}
        mock_post.return_value = response

        result = client.create_user(name="John", email="john@example.com")

    assert result == {"id": 10}
    mock_post.assert_called_once_with(
        f"{BASE_URL}/users",
        json={"name": "John", "email": "john@example.com"},
        headers={"Accept": "application/json", "Authorization": "Bearer xyz"},
        timeout=4,
    )


def test_create_user_raises_on_non_201():
    client = APIClient()

    with patch.object(client.session, "post") as mock_post:
        mock_post.return_value.status_code = 200

        with pytest.raises(Exception, match="Failed to create user"):
            client.create_user(name="John", email="john@example.com")


def test_update_email_success():
    client = APIClient(timeout=8)

    with patch.object(client.session, "put") as mock_put:
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {"email": "new@example.com"}
        mock_put.return_value = response

        result = client.update_email(user_id=1, new_email="new@example.com")

    assert result == {"email": "new@example.com"}
    mock_put.assert_called_once_with(
        f"{BASE_URL}/users/1/email",
        json={"email": "new@example.com"},
        headers={"Accept": "application/json"},
        timeout=8,
    )


def test_update_email_raises_on_non_200():
    client = APIClient()

    with patch.object(client.session, "put") as mock_put:
        mock_put.return_value.status_code = 404

        with pytest.raises(Exception, match="Failed to update email"):
            client.update_email(user_id=1, new_email="x@y.com")


def test_delete_user_success():
    client = APIClient(token="tok")

    with patch.object(client.session, "delete") as mock_delete:
        response = MagicMock()
        response.status_code = 204
        mock_delete.return_value = response

        result = client.delete_user(user_id=1)

    assert result is True
    mock_delete.assert_called_once_with(
        f"{BASE_URL}/users/1",
        headers={"Accept": "application/json", "Authorization": "Bearer tok"},
        timeout=3,
    )


def test_delete_user_raises_on_non_204():
    client = APIClient()

    with patch.object(client.session, "delete") as mock_delete:
        mock_delete.return_value.status_code = 500

        with pytest.raises(Exception, match="Failed to delete user"):
            client.delete_user(user_id=1)


def test_list_users_success_with_next_page():
    client = APIClient(timeout=6)

    with patch.object(client.session, "get") as mock_get:
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {"users": [{"id": 1}], "next_page": 2}
        mock_get.return_value = response

        users, next_page = client.list_users(page=3)

    assert users == [{"id": 1}]
    assert next_page == 2
    mock_get.assert_called_once_with(
        f"{BASE_URL}/users",
        headers={"Accept": "application/json"},
        params={"page": 3},
        timeout=6,
    )


def test_list_users_success_defaults_when_keys_missing():
    client = APIClient()

    with patch.object(client.session, "get") as mock_get:
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {}
        mock_get.return_value = response

        users, next_page = client.list_users()

    assert users == []
    assert next_page is None


def test_list_users_raises_on_non_200():
    client = APIClient()

    with patch.object(client.session, "get") as mock_get:
        mock_get.return_value.status_code = 500

        with pytest.raises(Exception, match="Failed to list users"):
            client.list_users(page=1)
