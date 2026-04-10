import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import requests
import RequestAPI

def test_get_data(monkeypatch):
    class MockResponse:
        def json(self):
            return {"id": 1}

    def mock_get(url):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    assert RequestAPI.get_data("http://example.com") == {"id": 1}

def test_post_data(monkeypatch):
    class MockResponse:
        def json(self):
            return {"title": "Test"}

    def mock_post(url, json):
        return MockResponse()

    monkeypatch.setattr(requests, "post", mock_post)
    assert RequestAPI.post_data("http://example.com", {"title": "Test"}) == {"title": "Test"}

def test_put_data(monkeypatch):
    class MockResponse:
        def json(self):
            return {"title": "Updated"}

    def mock_put(url, json):
        return MockResponse()

    monkeypatch.setattr(requests, "put", mock_put)
    assert RequestAPI.put_data("http://example.com", {"title": "Updated"}) == {"title": "Updated"}
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import pytest
import requests
import main as main_module
def test_main_prints_expected_json_outputs(monkeypatch, capsys):
    class MockResponse:
        def __init__(self, data):
            self._data = data
        def json(self):
            return self._data
    def mock_get(url):
        assert url == "https://jsonplaceholder.typicode.com/posts/1"
        return MockResponse({"id": 1})
    def mock_post(url, json):
        assert url == "https://jsonplaceholder.typicode.com/posts"
        assert json == {"title": "Test"}
        return MockResponse({"id": 101, "title": "Test"})
    def mock_put(url, json):
        assert url == "https://jsonplaceholder.typicode.com/posts/1"
        assert json == {"title": "Updated"}
        return MockResponse({"id": 1, "title": "Updated"})
    monkeypatch.setattr(requests, "get", mock_get)
    monkeypatch.setattr(requests, "post", mock_post)
    monkeypatch.setattr(requests, "put", mock_put)
    main_module.main()
    captured = capsys.readouterr()
    assert captured.out.splitlines() == ["{'id': 1}", "{'id': 101, 'title': 'Test'}", "{'id': 1, 'title': 'Updated'}"]
