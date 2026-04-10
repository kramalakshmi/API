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
        assert url == "http://example.com"
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    assert RequestAPI.get_data("http://example.com") == {"id": 1}

def test_post_data(monkeypatch):
    class MockResponse:
        def json(self):
            return {"created": True}

    def mock_post(url, json):
        assert url == "http://example.com"
        assert json == {"title": "Test"}
        return MockResponse()

    monkeypatch.setattr(requests, "post", mock_post)
    assert RequestAPI.post_data("http://example.com", {"title": "Test"}) == {"created": True}

def test_put_data(monkeypatch):
    class MockResponse:
        def json(self):
            return {"updated": True}

    def mock_put(url, json):
        assert url == "http://example.com"
        assert json == {"title": "Updated"}
        return MockResponse()

    monkeypatch.setattr(requests, "put", mock_put)
    assert RequestAPI.put_data("http://example.com", {"title": "Updated"}) == {"updated": True}