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

