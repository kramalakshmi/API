from src.RequestAPI import get_data, post_data, put_data

class MockResponse:
    def __init__(self, data):
        self.data = data
    def json(self):
        return self.data

def test_get_data(monkeypatch):
    def mock_get(url):
        return MockResponse({"id": 1})
    monkeypatch.setattr("src.RequestAPI.requests.get", mock_get)
    assert get_data("http://example.com") == {"id": 1}

def test_post_data(monkeypatch):
    def mock_post(url, json):
        return MockResponse({"title": json["title"]})
    monkeypatch.setattr("src.RequestAPI.requests.post", mock_post)
    assert post_data("http://example.com", {"title": "Test"}) == {"title": "Test"}

def test_put_data(monkeypatch):
    def mock_put(url, json):
        return MockResponse({"title": json["title"]})
    monkeypatch.setattr("src.RequestAPI.requests.put", mock_put)
    assert put_data("http://example.com", {"title": "Updated"}) == {"title": "Updated"}