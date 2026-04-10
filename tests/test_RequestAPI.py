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
def test_main_prints_expected_outputs(monkeypatch, capsys):
    monkeypatch.setattr(main_module, "get_data", lambda url: {"id": 1})
    monkeypatch.setattr(main_module, "post_data", lambda url, payload: {"title": "Test"})
    monkeypatch.setattr(main_module, "put_data", lambda url, payload: {"title": "Updated"})
    main_module.main()
    captured = capsys.readouterr()
    assert captured.out == "{'id': 1}\n{'title': 'Test'}\n{'title': 'Updated'}\n"
