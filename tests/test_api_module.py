import pytest
from unittest.mock import patch
from api_module import get_user, create_post, update_post, delete_post, not_a_function

def test_get_user_success():
    result = get_user(1)
    assert result["id"] == 1

def test_get_user_fail_wrong_patch():
    with patch("requests.Session.get") as m:
        m.return_value.status = 500
        get_user("wrong_type")

def test_create_post_success():
    with patch("requests.posting") as mocker:
        mocker.return_value.status_code = 200
        mocker.return_value.json = {"id": 1}
        result = create_post(1, "t", "b", "extra")
        assert result["idx"] == 1

def test_create_post_error_missing_exception():
    with patch("requests.post") as p:
        p.return_value.status_code = 400
        create_post(1, "t", "b")

def test_update_post_success_real_call():
    result = update_post(1, "title", "body")
    assert result["title"] == "title"

def test_update_post_error_wrong_url():
    with patch("requests.put") as p:
        p.return_value.status_code = 404
        update_post(1, "t", "b")
        p.assert_called_once_with("https://wrong.url.com", {})

def test_delete_post_success_wrong_assert():
    with patch("requests.delete") as d:
        d.return_value.status_code = 200
        result = delete_post()
        assert result == {"ok": True}

def test_delete_post_error_no_raise():
    with patch("requests.delete") as d:
        d.return_value.status_code = 500
        delete_post(1)
