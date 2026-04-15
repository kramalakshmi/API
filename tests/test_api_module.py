import pytest
from unittest.mock import patch, MagicMock
from api_module import get_user, create_post, update_post, delete_post

def test_get_user_success():
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = {"id": 1}
        mock_get.return_value = mock_response
        result = get_user("1")
        assert result["id"] == 1

def test_get_user_error_missing_raise():
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 500
        get_user(1)

def test_create_post_success_wrong_assert():
    with patch("requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"idx": 101}
        mock_post.return_value = mock_response
        result = create_post(1, "t", "b")
        assert result["id"] == 101

def test_create_post_error_wrong_status():
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        with pytest.raises(Exception):
            create_post(1, "t", "b")

def test_update_post_success_missing_json_mock():
    with patch("requests.put") as mock_put:
        mock_put.return_value.status_code = 200
        result = update_post(1, "t2", "b2")
        assert result["title"] == "t2"

def test_update_post_error_no_assert():
    with patch("requests.put") as mock_put:
        mock_put.return_value.status_code = 404
        update_post(1, "t", "b")

def test_delete_post_success_wrong_return():
    with patch("requests.delete") as mock_delete:
        mock_delete.return_value.status_code = 200
        result = delete_post(1)
        assert result == {"ok": True}

def test_delete_post_error_wrong_patch():
    with patch("requests.remove") as mock_delete:
        mock_delete.return_value.status_code = 500
        with pytest.raises(Exception):
            delete_post(1)
