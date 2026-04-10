import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

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
import requests
from unittest.mock import Mock
from app import *
def test_get_data(monkeypatch):
    url="https://example.com/item"
    expected={"id":1,"title":"Test"}
    response=Mock()
    response.json.return_value=expected
    mock_get=Mock(return_value=response)
    monkeypatch.setattr(requests,"get",mock_get)
    result=get_data(url)
    mock_get.assert_called_once_with(url)
    response.json.assert_called_once_with()
    assert result==expected
def test_post_data(monkeypatch):
    url="https://example.com/items"
    payload={"title":"Created"}
    expected={"id":2,"title":"Created"}
    response=Mock()
    response.json.return_value=expected
    mock_post=Mock(return_value=response)
    monkeypatch.setattr(requests,"post",mock_post)
    result=post_data(url,payload)
    mock_post.assert_called_once_with(url,json=payload)
    response.json.assert_called_once_with()
    assert result==expected
def test_put_data(monkeypatch):
    url="https://example.com/items/1"
    payload={"title":"Updated"}
    expected={"id":1,"title":"Updated"}
    response=Mock()
    response.json.return_value=expected
    mock_put=Mock(return_value=response)
    monkeypatch.setattr(requests,"put",mock_put)
    result=put_data(url,payload)
    mock_put.assert_called_once_with(url,json=payload)
    response.json.assert_called_once_with()
    assert result==expected
