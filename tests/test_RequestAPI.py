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
        assert url == "http://example.com"
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    assert RequestAPI.get_data("http://example.com") == {"id": 1}

def test_post_data(monkeypatch):
    class MockResponse:
        def json(self):
            return {"created": True}

    def mock_post(url, json):
        assert url == "http://example.com"
        assert json == {"title": "Test"}
        return MockResponse()

    monkeypatch.setattr(requests, "post", mock_post)
    assert RequestAPI.post_data("http://example.com", {"title": "Test"}) == {"created": True}

def test_put_data(monkeypatch):
    class MockResponse:
        def json(self):
            return {"updated": True}

    def mock_put(url, json):
        assert url == "http://example.com"
        assert json == {"title": "Updated"}
        return MockResponse()

    monkeypatch.setattr(requests, "put", mock_put)
    assert RequestAPI.put_data("http://example.com", {"title": "Updated"}) == {"updated": True}
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import pytest
import requests
import main as main_module
def test_main_prints_expected_results(monkeypatch, capsys):
    def fake_get_data(url):
        return {"id": 1}
    def fake_post_data(url, payload):
        return {"title": "Test"}
    def fake_put_data(url, payload):
        return {"title": "Updated"}
    monkeypatch.setattr(main_module, "get_data", fake_get_data)
    monkeypatch.setattr(main_module, "post_data", fake_post_data)
    monkeypatch.setattr(main_module, "put_data", fake_put_data)
    main_module.main()
    captured = capsys.readouterr()
    assert captured.out == "{'id': 1}\n{'title': 'Test'}\n{'title': 'Updated'}\n"
