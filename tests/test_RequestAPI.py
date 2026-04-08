from src import RequestAPI

class MockResponse:
    def __init__(self, data):
        self.data = data
    def json(self):
        return self.data

def test_get_data(monkeypatch):
    def mock_get(url):
        return MockResponse({"url": url})
    monkeypatch.setattr(RequestAPI.requests, "get", mock_get)
    assert RequestAPI.get_data("http://example.com") == {"url": "http://example.com"}

def test_post_data(monkeypatch):
    def mock_post(url, json):
        return MockResponse({"url": url, "json": json})
    monkeypatch.setattr(RequestAPI.requests, "post", mock_post)
    payload = {"title": "Test"}
    assert RequestAPI.post_data("http://example.com", payload) == {"url": "http://example.com", "json": payload}

def test_put_data(monkeypatch):
    def mock_put(url, json):
        return MockResponse({"url": url, "json": json})
    monkeypatch.setattr(RequestAPI.requests, "put", mock_put)
    payload = {"title": "Updated"}
    assert RequestAPI.put_data("http://example.com", payload) == {"url": "http://example.com", "json": payload}