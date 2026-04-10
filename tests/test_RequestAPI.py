import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pytest
from unittest.mock import Mock, patch
import RequestAPI

def test_get_data():
    response = Mock()
    response.json.return_value = {"id": 1}
    with patch("RequestAPI.requests.get", return_value=response) as mock_get:
        result = RequestAPI.get_data("http://example.com")
    mock_get.assert_called_once_with("http://example.com")
    assert result == {"id": 1}

def test_post_data():
    response = Mock()
    response.json.return_value = {"success": True}
    payload = {"title": "Test"}
    with patch("RequestAPI.requests.post", return_value=response) as mock_post:
        result = RequestAPI.post_data("http://example.com", payload)
    mock_post.assert_called_once_with("http://example.com", json=payload)
    assert result == {"success": True}

def test_put_data():
    response = Mock()
    response.json.return_value = {"updated": True}
    payload = {"title": "Updated"}
    with patch("RequestAPI.requests.put", return_value=response) as mock_put:
        result = RequestAPI.put_data("http://example.com", payload)
    mock_put.assert_called_once_with("http://example.com", json=payload)
    assert result == {"updated": True}

def test_main(capsys):
    with patch("RequestAPI.get_data", return_value={"id": 1}), \
         patch("RequestAPI.post_data", return_value={"title": "Test"}), \
         patch("RequestAPI.put_data", return_value={"title": "Updated"}):
        RequestAPI.main()
    captured = capsys.readouterr()
    assert "{'id': 1}" in captured.out
    assert "{'title': 'Test'}" in captured.out
    assert "{'title': 'Updated'}" in captured.out