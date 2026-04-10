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


def test_placeholder():
    pass

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import RequestAPI

def test_post_data(monkeypatch):
    url = "https://example.com/posts"
    payload = {"title": "Test"}
    expected = {"id": 1, "title": "Test"}

    class MockResponse:
        def json(self):
            return expected

    def mock_post(passed_url, json):
        assert passed_url == url
        assert json == payload
        return MockResponse()

    monkeypatch.setattr(RequestAPI.requests, "post", mock_post)
    assert RequestAPI.post_data(url, payload) == expected

def test_put_data(monkeypatch):
    url = "https://example.com/posts/1"
    payload = {"title": "Updated"}
    expected = {"id": 1, "title": "Updated"}

    class MockResponse:
        def json(self):
            return expected

    def mock_put(passed_url, json):
        assert passed_url == url
        assert json == payload
        return MockResponse()

    monkeypatch.setattr(RequestAPI.requests, "put", mock_put)
    assert RequestAPI.put_data(url, payload) == expected


