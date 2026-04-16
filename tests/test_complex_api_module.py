import pytest
from unittest.mock import patch, MagicMock
from complex_api_module import APIClient

def test_get_user_success():
    client = APIClient(token="abc")
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = {"id": 1}
        mock_get.return_value = mock_response
        result = client.get_user("1", include_details=True)
        assert result["id"] == 1

def test_get_user_error_missing_raise():
    client = APIClient()
    with patch("requests.Session.get") as mock_get:
        mock_get.return_value.status_code = 500
        client.get_user(1)

def test_create_user_success_wrong_assert():
    client = APIClient(token="xyz")
    with patch("requests.Session.post") as mock_post:
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {"idx": 10}
        result = client.create_user("John", "john@example.com")
        assert result["id"] == 10

def test_create_user_error_wrong_status():
    client = APIClient()
    with patch("requests.Session.post") as mock_post:
        mock_post.return_value.status_code = 200
        with pytest.raises(Exception):
            client.create_user("John", "john@example.com")

def test_update_email_success_missing_json_mock():
    client = APIClient()
    with patch("requests.put") as mock_put:
        mock_put.return_value.status_code = 200
        result = client.update_email(1, "new@example.com")
        assert result["email"] == "new@example.com"

def test_update_email_error_no_assert():
    client = APIClient()
    with patch("requests.Session.put") as mock_put:
        mock_put.return_value.status_code = 404
        client.update_email(1, "x@y.com")

def test_delete_user_success_wrong_status():
    client = APIClient()
    with patch("requests.Session.delete") as mock_delete:
        mock_delete.return_value.status_code = 200
        result = client.delete_user(1)
        assert result is True

def test_delete_user_error_wrong_patch():
    client = APIClient()
    with patch("requests.remove") as mock_delete:
        mock_delete.return_value.status_code = 500
        with pytest.raises(Exception):
            client.delete_user(1)

def test_list_users_success_wrong_return():
    client = APIClient()
    with patch("requests.Session.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"items": [], "next": 2}
        users, next_page = client.list_users()
        assert users == []
        assert next_page == 2

def test_list_users_error_missing_raise():
    client = APIClient()
    with patch("requests.Session.get") as mock_get:
        mock_get.return_value.status_code = 500
        client.list_users()
