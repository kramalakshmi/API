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
from src.RequestAPI import *
from unittest.mock import Mock, patch
def test_get_data_returns_json():
    url = "https://example.com/data"
    expected = {"id": 1, "name": "test"}
    with patch("src.RequestAPI.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = expected
        mock_get.return_value = mock_response
        result = get_data(url)
        mock_get.assert_called_once_with(url)
        assert result == expected
def test_post_data_returns_json():
    url = "https://example.com/data"
    payload = {"title": "Test"}
    expected = {"id": 101, "title": "Test"}
    with patch("src.RequestAPI.requests.post") as mock_post:
        mock_response = Mock()
        mock_response.json.return_value = expected
        mock_post.return_value = mock_response
        result = post_data(url, payload)
        mock_post.assert_called_once_with(url, json=payload)
        assert result == expected
