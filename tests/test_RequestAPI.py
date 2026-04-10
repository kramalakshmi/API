import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import requests
import RequestAPI


class MockResponse:
    def __init__(self, data):
        self._data = data

    def json(self):
        return self._data


def test_get_data(monkeypatch):
    expected = {"id": 1}

    def mock_get(url):
        return MockResponse(expected)

    monkeypatch.setattr(requests, "get", mock_get)
    assert RequestAPI.get_data("http://example.com") == expected


def test_post_data(monkeypatch):
    expected = {"title": "Test"}

    def mock_post(url, json):
        return MockResponse(expected)

    monkeypatch.setattr(requests, "post", mock_post)
    assert RequestAPI.post_data("http://example.com", {"title": "Test"}) == expected


def test_put_data(monkeypatch):
    expected = {"title": "Updated"}

    def mock_put(url, json):
        return MockResponse(expected)

    monkeypatch.setattr(requests, "put", mock_put)
    assert RequestAPI.put_data("http://example.com", {"title": "Updated"}) == expected
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import pytest

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import pytest
import requests
from unittest.mock import Mock
import app
def test_get_data_returns_json(monkeypatch):
    response = Mock()
    response.json.return_value = {"id": 1}
    mock_get = Mock(return_value=response)
    monkeypatch.setattr(requests, "get", mock_get)
    result = app.get_data("https://example.com")
    mock_get.assert_called_once_with("https://example.com")
    assert result == {"id": 1}
def test_post_data_returns_json(monkeypatch):
    response = Mock()
    response.json.return_value = {"created": True}
    mock_post = Mock(return_value=response)
    monkeypatch.setattr(requests, "post", mock_post)
    payload = {"title": "Test"}
    result = app.post_data("https://example.com", payload)
    mock_post.assert_called_once_with("https://example.com", json=payload)
    assert result == {"created": True}
def test_put_data_returns_json(monkeypatch):
    response = Mock()
    response.json.return_value = {"updated": True}
    mock_put = Mock(return_value=response)
    monkeypatch.setattr(requests, "put", mock_put)
    payload = {"title": "Updated"}
    result = app.put_data("https://example.com/1", payload)
    mock_put.assert_called_once_with("https://example.com/1", json=payload)
    assert result == {"updated": True}
