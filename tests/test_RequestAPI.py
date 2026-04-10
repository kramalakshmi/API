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

def test_put_data(monkeypatch):
    class Response:
        def json(self):
            return {"updated": True}

    def fake_put(url, json):
        return Response()

    monkeypatch.setattr(RequestAPI.requests, "put", fake_put)
    assert RequestAPI.put_data("http://example.com", {"a": 1}) == {"updated": True}

def test_main_block(monkeypatch, capsys):
    class Response:
        def __init__(self, data):
            self._data = data

        def json(self):
            return self._data

    monkeypatch.setattr("requests.get", lambda url: Response({"id": 1}))
    monkeypatch.setattr("requests.post", lambda url, json: Response({"title": "Test"}))
    monkeypatch.setattr("requests.put", lambda url, json: Response({"title": "Updated"}))
    runpy.run_module("RequestAPI", run_name="__main__")
    out = capsys.readouterr().out
    assert "{'id': 1}" in out
    assert "{'title': 'Test'}" in out
    assert "{'title': 'Updated'}" in out
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
import pytest
from unittest.mock import Mock, patch
from src import *
def test_get_data():
    url="https://example.com/data"
    expected={"id":1,"name":"test"}
    mock_response=Mock()
    mock_response.json.return_value=expected
    with patch("src.requests.get",return_value=mock_response) as mock_get:
        result=get_data(url)
    mock_get.assert_called_once_with(url)
    assert result==expected
def test_post_data():
    url="https://example.com/data"
    payload={"title":"Test"}
    expected={"id":101,"title":"Test"}
    mock_response=Mock()
    mock_response.json.return_value=expected
    with patch("src.requests.post",return_value=mock_response) as mock_post:
        result=post_data(url,payload)
    mock_post.assert_called_once_with(url,json=payload)
    assert result==expected
def test_put_data():
    url="https://example.com/data/1"
    payload={"title":"Updated"}
    expected={"id":1,"title":"Updated"}
    mock_response=Mock()
    mock_response.json.return_value=expected
    with patch("src.requests.put",return_value=mock_response) as mock_put:
        result=put_data(url,payload)
    mock_put.assert_called_once_with(url,json=payload)
    assert result==expected
