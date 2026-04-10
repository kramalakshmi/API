import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import RequestAPI

class DummyResponse:
    def __init__(self, data):
        self.data=data
    def json(self):
        return self.data


def test_put_data(monkeypatch):
    def fake_put(url,json):
        assert url=="http://example.com/1"
        assert json=={"title":"Updated"}
        return DummyResponse({"updated":True})
    monkeypatch.setattr(RequestAPI.requests,"put",fake_put)
    assert RequestAPI.put_data("http://example.com/1",{"title":"Updated"})=={"updated":True}
