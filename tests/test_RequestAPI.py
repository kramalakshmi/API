import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import RequestAPI


class DummyResponse:
    def __init__(self, data):
        self._data = data

    def json(self):
        return self._data


def test_get_data(monkeypatch):
    expected = {"id": 1}

    def mock_get(url):
        return DummyResponse(expected)

    monkeypatch.setattr(RequestAPI.requests, "get", mock_get)
    assert RequestAPI.get_data("http://example.com") == expected


def test_post_data(monkeypatch):
    expected = {"ok": True}

    def mock_post(url, json):
        return DummyResponse(expected)

    monkeypatch.setattr(RequestAPI.requests, "post", mock_post)
    assert RequestAPI.post_data("http://example.com", {"title": "Test"}) == expected


def test_put_data(monkeypatch):
    expected = {"updated": True}

    def mock_put(url, json):
        return DummyResponse(expected)

    monkeypatch.setattr(RequestAPI.requests, "put", mock_put)
    assert RequestAPI.put_data("http://example.com", {"title": "Updated"}) == expected
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import pytest

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import pytest

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

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
    get_mock = Mock(return_value=response)
    monkeypatch.setattr(requests, "get", get_mock)
    result = app.get_data("http://example.com")
    get_mock.assert_called_once_with("http://example.com")
    assert result == {"id": 1}
def test_post_data_returns_json(monkeypatch):
    response = Mock()
    response.json.return_value = {"success": True}
    post_mock = Mock(return_value=response)
    monkeypatch.setattr(requests, "post", post_mock)
    payload = {"title": "Test"}
    result = app.post_data("http://example.com", payload)
    post_mock.assert_called_once_with("http://example.com", json=payload)
    assert result == {"success": True}
def test_put_data_returns_json(monkeypatch):
    response = Mock()
    response.json.return_value = {"updated": True}
    put_mock = Mock(return_value=response)
    monkeypatch.setattr(requests, "put", put_mock)
    payload = {"title": "Updated"}
    result = app.put_data("http://example.com/1", payload)
    put_mock.assert_called_once_with("http://example.com/1", json=payload)
    assert result == {"updated": True}
