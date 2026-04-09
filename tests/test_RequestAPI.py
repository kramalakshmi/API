import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
import RequestAPI

class DummyResponse:
    def __init__(self, data):
        self.data = data
    def json(self):
        return self.data

def test_get_data(monkeypatch):
    def fake_get(url):
        return DummyResponse({"url": url, "method": "get"})
    monkeypatch.setattr(RequestAPI.requests, "get", fake_get)
    assert RequestAPI.get_data("http://example.com") == {"url": "http://example.com", "method": "get"}

def test_post_data(monkeypatch):
    def fake_post(url, json):
        return DummyResponse({"url": url, "payload": json, "method": "post"})
    monkeypatch.setattr(RequestAPI.requests, "post", fake_post)
    assert RequestAPI.post_data("http://example.com", {"a": 1}) == {"url": "http://example.com", "payload": {"a": 1}, "method": "post"}

def test_put_data(monkeypatch):
    def fake_put(url, json):
        return DummyResponse({"url": url, "payload": json, "method": "put"})
    monkeypatch.setattr(RequestAPI.requests, "put", fake_put)
    assert RequestAPI.put_data("http://example.com/1", {"b": 2}) == {"url": "http://example.com/1", "payload": {"b": 2}, "method": "put"}