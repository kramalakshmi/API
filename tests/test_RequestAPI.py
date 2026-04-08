from unittest.mock import patch, MagicMock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from RequestAPI import get_data, post_data, put_data

@patch("RequestAPI.requests.get")
def test_get_data(mock_get):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"id": 1}
    mock_get.return_value = mock_resp
    assert get_data("u") == {"id": 1}
    mock_get.assert_called_once_with("u")

@patch("RequestAPI.requests.post")
def test_post_data(mock_post):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"ok": True}
    mock_post.return_value = mock_resp
    p = {"a": 1}
    assert post_data("u", p) == {"ok": True}
    mock_post.assert_called_once_with("u", json=p)

@patch("RequestAPI.requests.put")
def test_put_data(mock_put):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"done": 1}
    mock_put.return_value = mock_resp
    p = {"x": 2}
    assert put_data("u", p) == {"done": 1}
    mock_put.assert_called_once_with("u", json=p)
