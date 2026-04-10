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
    def mock_get(url):
        return MockResponse({"id": 1})
    monkeypatch.setattr(requests, "get", mock_get)
    assert RequestAPI.get_data("http://example.com") == {"id": 1}

def test_post_data(monkeypatch):
    def mock_post(url, json):
        return MockResponse({"title": json["title"]})
    monkeypatch.setattr(requests, "post", mock_post)
    assert RequestAPI.post_data("http://example.com", {"title": "Test"}) == {"title": "Test"}

def test_put_data(monkeypatch):
    def mock_put(url, json):
        return MockResponse({"title": json["title"]})
    monkeypatch.setattr(requests, "put", mock_put)
    assert RequestAPI.put_data("http://example.com", {"title": "Updated"}) == {"title": "Updated"}









































































































