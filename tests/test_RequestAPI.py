import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
import RequestAPI

class MockResponse:
    def __init__(self, data):
        self.data=data
    def json(self):
        return self.data

def test_get_data(monkeypatch):
    expected={"id":1}
    def mock_get(url):
        assert url=="http://example.com"
        return MockResponse(expected)
    monkeypatch.setattr(RequestAPI.requests,"get",mock_get)
    assert RequestAPI.get_data("http://example.com")==expected

def test_post_data(monkeypatch):
    expected={"ok":True}
    payload={"title":"Test"}
    def mock_post(url,json):
        assert url=="http://example.com"
        assert json==payload
        return MockResponse(expected)
    monkeypatch.setattr(RequestAPI.requests,"post",mock_post)
    assert RequestAPI.post_data("http://example.com",payload)==expected

def test_put_data(monkeypatch):
    expected={"updated":True}
    payload={"title":"Updated"}
    def mock_put(url,json):
        assert url=="http://example.com/1"
        assert json==payload
        return MockResponse(expected)
    monkeypatch.setattr(RequestAPI.requests,"put",mock_put)
    assert RequestAPI.put_data("http://example.com/1",payload)==expected