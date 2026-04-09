import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
import RequestAPI

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
            return {"title": "Test"}
    def fake_post(url, json):
        return Response()
    monkeypatch.setattr(RequestAPI.requests, "post", fake_post)
    assert RequestAPI.post_data("http://example.com", {"title": "Test"}) == {"title": "Test"}

def test_put_data(monkeypatch):
    class Response:
        def json(self):
            return {"title": "Updated"}
    def fake_put(url, json):
        return Response()
    monkeypatch.setattr(RequestAPI.requests, "put", fake_put)
    assert RequestAPI.put_data("http://example.com", {"title": "Updated"}) == {"title": "Updated"}