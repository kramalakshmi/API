import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

import RequestAPI
import runpy

class MockResponse:
    def __init__(self, data):
        self._data = data

    def json(self):
        return self._data

def test_get_data(monkeypatch):
    def mock_get(url):
        return MockResponse({"url": url})
    monkeypatch.setattr(RequestAPI.requests, "get", mock_get)
    assert RequestAPI.get_data("http://example.com") == {"url": "http://example.com"}

def test_post_data(monkeypatch):
    def mock_post(url, json):
        return MockResponse({"url": url, "json": json})
    monkeypatch.setattr(RequestAPI.requests, "post", mock_post)
    assert RequestAPI.post_data("http://example.com", {"a": 1}) == {"url": "http://example.com", "json": {"a": 1}}

def test_put_data(monkeypatch):
    def mock_put(url, json):
        return MockResponse({"url": url, "json": json})
    monkeypatch.setattr(RequestAPI.requests, "put", mock_put)
    assert RequestAPI.put_data("http://example.com", {"a": 2}) == {"url": "http://example.com", "json": {"a": 2}}

def test_main_block(monkeypatch, capsys):
    monkeypatch.setattr(RequestAPI.requests, "get", lambda url: MockResponse({"get": url}))
    monkeypatch.setattr(RequestAPI.requests, "post", lambda url, json: MockResponse({"post": url, "json": json}))
    monkeypatch.setattr(RequestAPI.requests, "put", lambda url, json: MockResponse({"put": url, "json": json}))
    runpy.run_module("RequestAPI", run_name="__main__")
    out = capsys.readouterr().out.strip().splitlines()
    assert out == [
        "{'get': 'https://jsonplaceholder.typicode.com/posts/1'}",
        "{'post': 'https://jsonplaceholder.typicode.com/posts', 'json': {'title': 'Test'}}",
        "{'put': 'https://jsonplaceholder.typicode.com/posts/1', 'json': {'title': 'Updated'}}",
    ]