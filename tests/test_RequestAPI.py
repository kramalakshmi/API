import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import requests
import RequestAPI

def test_get_data(monkeypatch):
    class MockResponse:
        def json(self):
            return {"id": 1}

    def mock_get(url):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    assert RequestAPI.get_data("http://example.com") == {"id": 1}


def test_post_data(monkeypatch):
    class MockResponse:
        def json(self):
            return {"result": "posted"}

    def mock_post(url, json):
        assert url == "https://example.com"
        assert json == {"title": "Test"}
        return MockResponse()

    monkeypatch.setattr(RequestAPI.requests, "post", mock_post)
    assert RequestAPI.post_data("https://example.com", {"title": "Test"}) == {"result": "posted"}


def test_put_data(monkeypatch):
    class MockResponse:
        def json(self):
            return {"result": "updated"}

    def mock_put(url, json):
        assert url == "https://example.com/1"
        assert json == {"title": "Updated"}
        return MockResponse()

    monkeypatch.setattr(RequestAPI.requests, "put", mock_put)
    assert RequestAPI.put_data("https://example.com/1", {"title": "Updated"}) == {"result": "updated"}






