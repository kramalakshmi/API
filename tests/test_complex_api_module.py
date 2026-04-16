import pytest
from unittest.mock import MagicMock, patch


def test_headers_without_token():
    from src.complex_api_module import APIClient

    client = APIClient()
    assert client._headers() == {"Accept": "application/json"}


def test_headers_with_token():
    from src.complex_api_module import APIClient

    client = APIClient(token="token123")
    assert client._headers() == {
        "Accept": "application/json",
        "Authorization": "Bearer token123",
    }


def test_get_user_success_without_details():
    from src.complex_api_module import APIClient, BASE_URL

    client = APIClient(token="abc", retries=2, timeout=7)
    expected = {"id": 1, "name": "Alice"}

    with patch.object(client.session, "get") as mock_get:
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = expected
        mock_get.return_value = response

        result = client.get_user(user_id=1)

    assert result == expected
    mock_get.assert_called_once_with(
        f"{BASE_URL}/users/1",
        headers={"Accept": "application/json", "Authorization": "Bearer abc"},
        params={},
        timeout=7,
    )


def test_get_user_success_with_details():
    from src.complex_api_module import APIClient, BASE_URL

    client = APIClient(retries=1, timeout=5)
    expected = {"id": 2, "details": True}

    with patch.object(client.session, "get") as mock_get:
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = expected
        mock_get.return_value = response

        result = client.get_user(user_id="user-2", include_details=True)

    assert result == expected
    mock_get.assert_called_once_with(
        f"{BASE_URL}/users/user-2",
        headers={"Accept": "application/json"},
        params={"details": "1"},
        timeout=5,
    )


def test_get_user_retries_then_succeeds():
    from src.complex_api_module import APIClient

    client = APIClient(retries=3)

    with patch.object(client.session, "get") as mock_get, patch("src.complex_api_module.time.sleep") as mock_sleep:
        first = MagicMock(status_code=500)
        second = MagicMock(status_code=200)
        second.json.return_value = {"ok": True}
        mock_get.side_effect = [first, second]

        result = client.get_user(user_id=10)

    assert result == {"ok": True}
    assert mock_get.call_count == 2
    mock_sleep.assert_called_once_with(0.1)


def test_get_user_raises_after_all_retries_fail():
    from src.complex_api_module import APIClient

    client = APIClient(retries=2)

    with patch.object(client.session, "get") as mock_get, patch("src.complex_api_module.time.sleep") as mock_sleep:
        mock_get.return_value = MagicMock(status_code=500)

        with pytest.raises(Exception, match="Failed to fetch user"):
            client.get_user(user_id=99)

    assert mock_get.call_count == 2
    assert mock_sleep.call_count == 2


def test_create_user_success():
    from src.complex_api_module import APIClient, BASE_URL

    client = APIClient(token="secret", timeout=4)
    expected = {"id": 99, "name": "John", "email": "john@example.com"}

    with patch.object(client.session, "post") as mock_post:
        response = MagicMock()
        response.status_code = 201
        response.json.return_value = expected
        mock_post.return_value = response

        result = client.create_user(name="John", email="john@example.com")

    assert result == expected
    mock_post.assert_called_once_with(
        f"{BASE_URL}/users",
        json={"name": "John", "email": "john@example.com"},
        headers={"Accept": "application/json", "Authorization": "Bearer secret"},
        timeout=4,
    )


def test_create_user_raises_on_failure():
    from src.complex_api_module import APIClient

    client = APIClient()

    with patch.object(client.session, "post") as mock_post:
        mock_post.return_value = MagicMock(status_code=400)

        with pytest.raises(Exception, match="Failed to create user"):
            client.create_user(name="John", email="john@example.com")


def test_update_email_success():
    from src.complex_api_module import APIClient, BASE_URL

    client = APIClient(timeout=9)
    expected = {"id": 1, "email": "new@example.com"}

    with patch.object(client.session, "put") as mock_put:
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = expected
        mock_put.return_value = response

        result = client.update_email(user_id=1, new_email="new@example.com")

    assert result == expected
    mock_put.assert_called_once_with(
        f"{BASE_URL}/users/1/email",
        json={"email": "new@example.com"},
        headers={"Accept": "application/json"},
        timeout=9,
    )


def test_update_email_raises_on_failure():
    from src.complex_api_module import APIClient

    client = APIClient()

    with patch.object(client.session, "put") as mock_put:
        mock_put.return_value = MagicMock(status_code=404)

        with pytest.raises(Exception, match="Failed to update email"):
            client.update_email(user_id=1, new_email="x@y.com")


def test_delete_user_success():
    from src.complex_api_module import APIClient, BASE_URL

    client = APIClient(token="tok", timeout=6)

    with patch.object(client.session, "delete") as mock_delete:
        mock_delete.return_value = MagicMock(status_code=204)

        result = client.delete_user(user_id="1")

    assert result is True
    mock_delete.assert_called_once_with(
        f"{BASE_URL}/users/1",
        headers={"Accept": "application/json", "Authorization": "Bearer tok"},
        timeout=6,
    )


def test_delete_user_raises_on_failure():
    from src.complex_api_module import APIClient

    client = APIClient()

    with patch.object(client.session, "delete") as mock_delete:
        mock_delete.return_value = MagicMock(status_code=500)

        with pytest.raises(Exception, match="Failed to delete user"):
            client.delete_user(user_id=1)


def test_list_users_success_with_next_page():
    from src.complex_api_module import APIClient, BASE_URL

    client = APIClient(timeout=8)

    with patch.object(client.session, "get") as mock_get:
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {"users": [{"id": 1}], "next_page": 3}
        mock_get.return_value = response

        users, next_page = client.list_users(page=2)

    assert users == [{"id": 1}]
    assert next_page == 3
    mock_get.assert_called_once_with(
        f"{BASE_URL}/users",
        headers={"Accept": "application/json"},
        params={"page": 2},
        timeout=8,
    )


def test_list_users_success_defaults_when_keys_missing():
    from src.complex_api_module import APIClient

    client = APIClient()

    with patch.object(client.session, "get") as mock_get:
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {}
        mock_get.return_value = response

        users, next_page = client.list_users()

    assert users == []
    assert next_page is None


def test_list_users_raises_on_failure():
    from src.complex_api_module import APIClient

    client = APIClient()

    with patch.object(client.session, "get") as mock_get:
        mock_get.return_value = MagicMock(status_code=500)

        with pytest.raises(Exception, match="Failed to list users"):
            client.list_users(page=1)
