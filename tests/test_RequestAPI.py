import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
import RequestAPI
import pytest
from unittest.mock import Mock

def test_get_data(monkeypatch):
    response = Mock()
    response.json.return_value = {"id": 1}
    monkeypatch.setattr(RequestAPI.requests, "get", Mock(return_value=response))
    assert RequestAPI.get_data("http://example.com") == {"id": 1}

def test_post_data(monkeypatch):
    response = Mock()
    response.json.return_value = {"title": "Test"}
    post_mock = Mock(return_value=response)
    monkeypatch.setattr(RequestAPI.requests, "post", post_mock)
    payload = {"title": "Test"}
    assert RequestAPI.post_data("http://example.com", payload) == {"title": "Test"}
    post_mock.assert_called_once_with("http://example.com", json=payload)

def test_put_data(monkeypatch):
    response = Mock()
    response.json.return_value = {"title": "Updated"}
    put_mock = Mock(return_value=response)
    monkeypatch.setattr(RequestAPI.requests, "put", put_mock)
    payload = {"title": "Updated"}
    assert RequestAPI.put_data("http://example.com", payload) == {"title": "Updated"}
    put_mock.assert_called_once_with("http://example.com", json=payload)