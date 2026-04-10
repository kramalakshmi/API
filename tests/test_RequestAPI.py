import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
import RequestAPI
print("Imported module:", RequestAPI)

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



import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from src import *
import requests
from unittest.mock import Mock

def test_get_data(monkeypatch):
    mock_response = Mock()
    mock_response.json.return_value = {"id": 1, "title": "Test"}
    mock_get = Mock(return_value=mock_response)
    monkeypatch.setattr(requests, "get", mock_get)
    result = get_data("https://example.com/data")
    mock_get.assert_called_once_with("https://example.com/data")
    assert result == {"id": 1, "title": "Test"}

def test_post_data(monkeypatch):
    payload = {"title": "New"}
    mock_response = Mock()
    mock_response.json.return_value = {"id": 2, "title": "New"}
    mock_post = Mock(return_value=mock_response)
    monkeypatch.setattr(requests, "post", mock_post)
    result = post_data("https://example.com/data", payload)
    mock_post.assert_called_once_with("https://example.com/data", json=payload)
    assert result == {"id": 2, "title": "New"}
