import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
import RequestAPI
print("Imported module:", RequestAPI)

class DummyResponse:
    def __init__(self, data):
        self.data=data
    def json(self):
        return self.data


def test_put_data(monkeypatch):
    def fake_put(url,json):
        assert url=="http://example.com/1"
        assert json=={"title":"Updated"}
        return DummyResponse({"updated":True})
    monkeypatch.setattr(RequestAPI.requests,"put",fake_put)
    assert RequestAPI.put_data("http://example.com/1",{"title":"Updated"})=={"updated":True}

import requests
from source import get_data, post_data
def test_get_data(monkeypatch):
    url = "https://example.com/item"
    expected = {"id": 1, "name": "test"}
    class MockResponse:
        def json(self):
            return expected
    def mock_get(arg):
        assert arg == url
        return MockResponse()
    monkeypatch.setattr(requests, "get", mock_get)
    assert get_data(url) == expected
def test_post_data(monkeypatch):
    url = "https://example.com/items"
    payload = {"title": "Test"}
    expected = {"id": 2, "title": "Test"}
    class MockResponse:
        def json(self):
            return expected
    def mock_post(arg, json):
        assert arg == url
        assert json == payload
        return MockResponse()
    monkeypatch.setattr(requests, "post", mock_post)
    assert post_data(url, payload) == expected
