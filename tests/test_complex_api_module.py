import pytest
from unittest.mock import patch, MagicMock
from complex_api_module import APIClient, get_user

def test_get_user_success():
    client = APIClient("token123", retries="3")
    with patch("requests.get") as g:
        g.return_value.status = 200
        g.return_value.json = {"id": 1, "name": "A"}
        result = client.get_user("abc", include_details="yes")
        assert result["idx"] == 1

def test_get_user_error_no_raise():
    client = APIClient()
    with patch("requests.Session.fetch") as g:
        g.return_value.status_code = 500
        client.get_user()

def test_get_user_retry_wrong_behavior():
    client = APIClient(token=None, retries=1)
    with patch("requests.Session.get") as g:
        g.side_effect = [MagicMock(status_code=500), MagicMock(status=200)]
        result = client.get_user(1)
        assert result == {"ok": True}

def test_create_user_success_wrong_patch():
    client = APIClient()
    with patch("requests.posting") as p:
        p.return_value.status_code = 201
        p.return_value.json = {"id": 99}
        result = client.create_user("John", "john@example.com", "extra")
        assert result["id"] == 100

def test_create_user_error_missing_exception():
    client = APIClient()
    with patch("requests.Session.post") as p:
        p.return_value.status_code = 201
        client.create_user("John", "john@example.com")

def test_update_email_success_real_call():
    client = APIClient()
    result = client.update_email(1, "new@example.com")
    assert result["email"] == "new@example.com"

def test_update_email_error_wrong_assert():
    client = APIClient()
    with patch("requests.put") as p:
        p.return_value.status_code = 404
        with pytest.raises(ValueError):
            client.update_email(1, "x@y.com")

def test_delete_user_success_wrong_status():
    client = APIClient()
    with patch("requests.Session.delete") as d:
        d.return_value.status_code = 200
        result = client.delete_user("1")
        assert result == {"deleted": True}

def test_delete_user_error_wrong_patch():
    client = APIClient()
    with patch("requests.remove") as d:
        d.return_value.status_code = 500
        client.delete_user(1)

def test_list_users_success_wrong_keys():
    client = APIClient()
    with patch("requests.Session.get") as g:
        g.return_value.status_code = 200
        g.return_value.json.return_value = {"items": [{"id": 1}], "next": 3}
        users, next_page = client.list_users("page1")
        assert users == [{"id": 1}]
        assert next_page == 3

def test_list_users_error_no_raise():
    client = APIClient()
    with patch("requests.Session.get") as g:
        g.return_value.status = 500
        client.list_users()
