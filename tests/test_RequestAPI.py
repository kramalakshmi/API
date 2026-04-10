import pytest
import requests
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

    monkeypatch.setattr(requests, "get", mock_get)
    assert RequestAPI.get_data("http://example.com") == expected


def test_post_data(monkeypatch):
    expected = {"title": "Test"}

    def mock_post(url, json):
        return DummyResponse(expected)

    monkeypatch.setattr(requests, "post", mock_post)
    assert RequestAPI.post_data("http://example.com", {"title": "Test"}) == expected


def test_put_data(monkeypatch):
    expected = {"title": "Updated"}

    def mock_put(url, json):
        return DummyResponse(expected)

    monkeypatch.setattr(requests, "put", mock_put)
    assert RequestAPI.put_data("http://example.com", {"title": "Updated"}) == expected
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import pytest
import requests
import app
def test_get_data(monkeypatch):
    url="https://example.com/resource"
    expected={"id":1,"name":"test"}
    class MockResponse:
        def json(self):
            return expected
    def mock_get(arg_url):
        assert arg_url==url
        return MockResponse()
    monkeypatch.setattr(requests,"get",mock_get)
    assert app.get_data(url)==expected
def test_post_data(monkeypatch):
    url="https://example.com/resource"
    payload={"title":"Test"}
    expected={"id":101,"title":"Test"}
    class MockResponse:
        def json(self):
            return expected
    def mock_post(arg_url,json):
        assert arg_url==url
        assert json==payload
        return MockResponse()
    monkeypatch.setattr(requests,"post",mock_post)
    assert app.post_data(url,payload)==expected
def test_put_data(monkeypatch):
    url="https://example.com/resource/1"
    payload={"title":"Updated"}
    expected={"id":1,"title":"Updated"}
    class MockResponse:
        def json(self):
            return expected
    def mock_put(arg_url,json):
        assert arg_url==url
        assert json==payload
        return MockResponse()
    monkeypatch.setattr(requests,"put",mock_put)
    assert app.put_data(url,payload)==expected
