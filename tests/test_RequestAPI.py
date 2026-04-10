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
    class MockResponse:
        def json(self):
            return {"id": 1, "title": "Test"}
    def mock_get(url):
        assert url == "https://example.com/item"
        return MockResponse()
    monkeypatch.setattr(requests, "get", mock_get)
    assert get_data("https://example.com/item") == {"id": 1, "title": "Test"}
def test_post_data(monkeypatch):
    class MockResponse:
        def json(self):
            return {"success": True}
    def mock_post(url, json):
        assert url == "https://example.com/items"
        assert json == {"title": "New"}
        return MockResponse()
    monkeypatch.setattr(requests, "post", mock_post)
    assert post_data("https://example.com/items", {"title": "New"}) == {"success": True}
