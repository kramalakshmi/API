import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
import RequestAPI

class DummyResponse:
    def __init__(self, data):
        self.data=data
    def json(self):
        return self.data

def test_get_data(monkeypatch):
    def fake_get(url):
        assert url=="http://example.com"
        return DummyResponse({"ok":1})
    monkeypatch.setattr(RequestAPI.requests,"get",fake_get)
    assert RequestAPI.get_data("http://example.com")=={"ok":1}

def test_post_data(monkeypatch):
    def fake_post(url,json):
        assert url=="http://example.com"
        assert json=={"a":1}
        return DummyResponse({"created":True})
    monkeypatch.setattr(RequestAPI.requests,"post",fake_post)
    assert RequestAPI.post_data("http://example.com",{"a":1})=={"created":True}

def test_put_data(monkeypatch):
    def fake_put(url,json):
        assert url=="http://example.com/1"
        assert json=={"title":"Updated"}
        return DummyResponse({"updated":True})
    monkeypatch.setattr(RequestAPI.requests,"put",fake_put)
    assert RequestAPI.put_data("http://example.com/1",{"title":"Updated"})=={"updated":True}