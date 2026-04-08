import src.RequestAPI as RequestAPI

class DummyResponse:
    def __init__(self, data):
        self.data = data
    def json(self):
        return self.data

def test_get_data(monkeypatch):
    expected = {"id": 1}
    def fake_get(url):
        return DummyResponse(expected)
    monkeypatch.setattr(RequestAPI.requests, "get", fake_get)
    assert RequestAPI.get_data("http://example.com") == expected

def test_post_data(monkeypatch):
    expected = {"ok": True}
    def fake_post(url, json):
        return DummyResponse(expected)
    monkeypatch.setattr(RequestAPI.requests, "post", fake_post)
    assert RequestAPI.post_data("http://example.com", {"title": "Test"}) == expected

def test_put_data(monkeypatch):
    expected = {"updated": True}
    def fake_put(url, json):
        return DummyResponse(expected)
    monkeypatch.setattr(RequestAPI.requests, "put", fake_put)
    assert RequestAPI.put_data("http://example.com", {"title": "Updated"}) == expected