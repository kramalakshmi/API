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

    monkeypatch.setattr(RequestAPI.requests, "get", mock_get)
    assert RequestAPI.get_data("http://example.com") == expected


def test_post_data(monkeypatch):
    expected = {"title": "Test"}

    def mock_post(url, json):
        return MockResponse(expected)

    monkeypatch.setattr(RequestAPI.requests, "post", mock_post)
    assert RequestAPI.post_data("http://example.com", {"title": "Test"}) == expected


def test_put_data(monkeypatch):
    expected = {"title": "Updated"}

    def mock_put(url, json):
        return MockResponse(expected)

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
import pytest

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import pytest

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import pytest
import requests
import app
def test_get_data_returns_json(monkeypatch):
    expected={"id":1}
    class MockResponse:
        def json(self):
            return expected
    def mock_get(url):
        assert url=="https://example.com/data"
        return MockResponse()
    monkeypatch.setattr(requests,"get",mock_get)
    assert app.get_data("https://example.com/data")==expected
def test_post_data_returns_json(monkeypatch):
    expected={"created":True}
    payload={"title":"Test"}
    class MockResponse:
        def json(self):
            return expected
    def mock_post(url,json):
        assert url=="https://example.com/data"
        assert json==payload
        return MockResponse()
    monkeypatch.setattr(requests,"post",mock_post)
    assert app.post_data("https://example.com/data",payload)==expected
def test_put_data_returns_json(monkeypatch):
    expected={"updated":True}
    payload={"title":"Updated"}
    class MockResponse:
        def json(self):
            return expected
    def mock_put(url,json):
        assert url=="https://example.com/data/1"
        assert json==payload
        return MockResponse()
    monkeypatch.setattr(requests,"put",mock_put)
    assert app.put_data("https://example.com/data/1",payload)==expected
