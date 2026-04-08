import src.RequestAPI as RequestAPI

class DummyResponse:
    def __init__(self, data):
        self.data = data
    def json(self):
        return self.data

def test_get_data(monkeypatch):
    def fake_get(url):
        return DummyResponse({"url": url})
    monkeypatch.setattr(RequestAPI.requests, "get", fake_get)
    assert RequestAPI.get_data("http://example.com") == {"url": "http://example.com"}

def test_post_data(monkeypatch):
    def fake_post(url, json):
        return DummyResponse({"url": url, "json": json})
    monkeypatch.setattr(RequestAPI.requests, "post", fake_post)
    payload = {"title": "Test"}
    assert RequestAPI.post_data("http://example.com", payload) == {"url": "http://example.com", "json": payload}

def test_put_data(monkeypatch):
    def fake_put(url, json):
        return DummyResponse({"url": url, "json": json})
    monkeypatch.setattr(RequestAPI.requests, "put", fake_put)
    payload = {"title": "Updated"}
    assert RequestAPI.put_data("http://example.com", payload) == {"url": "http://example.com", "json": payload}