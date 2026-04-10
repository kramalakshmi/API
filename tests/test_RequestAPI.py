import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

import RequestAPI
import runpy

def test_get_data(monkeypatch):
    class Response:
        def json(self):
            return {"id": 1}

    def fake_get(url):
        return Response()

    monkeypatch.setattr(RequestAPI.requests, "get", fake_get)
    assert RequestAPI.get_data("http://example.com") == {"id": 1}

def test_post_data(monkeypatch):
    class Response:
        def json(self):
            return {"created": True}

    def fake_post(url, json):
        return Response()

    monkeypatch.setattr(RequestAPI.requests, "post", fake_post)
    assert RequestAPI.post_data("http://example.com", {"a": 1}) == {"created": True}


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from src import *
import requests
def test_put_data_calls_requests_put_with_json_and_returns_json(monkeypatch):
    url="https://example.com/resource/1"
    payload={"title":"Updated"}
    expected={"id":1,"title":"Updated"}
    class MockResponse:
        def json(self):
            return expected
    def mock_put(call_url, json):
        assert call_url==url
        assert json==payload
        return MockResponse()
    monkeypatch.setattr(requests,"put",mock_put)
    assert put_data(url,payload)==expected
def test_put_data_propagates_json_exception(monkeypatch):
    url="https://example.com/resource/1"
    payload={"title":"Updated"}
    class MockResponse:
        def json(self):
            raise ValueError("invalid json")
    def mock_put(call_url, json):
        assert call_url==url
        assert json==payload
        return MockResponse()
    monkeypatch.setattr(requests,"put",mock_put)
    import pytest
    with pytest.raises(ValueError,match="invalid json"):
        put_data(url,payload)
