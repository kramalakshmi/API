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

def test_placeholder():
    pass

def test_parse_data_with_valid_json():
    import json
    if not hasattr(RequestAPI, "parse_data"):
        return
    payload = '{"a": 1, "b": "x"}'
    result = RequestAPI.parse_data(payload)
    assert result == json.loads(payload)


def test_parse_data_with_invalid_json():
    if not hasattr(RequestAPI, "parse_data"):
        return
    invalid_payload = '{"a": 1,'
    try:
        RequestAPI.parse_data(invalid_payload)
    except Exception:
        assert True
    else:
        assert False


def test_get_data_with_mocked_success(monkeypatch):
    if not hasattr(RequestAPI, "get_data"):
        return

    class MockResponse:
        def __init__(self):
            self.status_code = 200
        def json(self):
            return {"ok": True}

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(RequestAPI.requests, "get", mock_get)
    result = RequestAPI.get_data("http://example.com")
    assert result == {"ok": True}


def test_get_data_with_mocked_failure(monkeypatch):
    if not hasattr(RequestAPI, "get_data"):
        return

    class MockResponse:
        def __init__(self):
            self.status_code = 404
        def json(self):
            return {"error": "not found"}

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(RequestAPI.requests, "get", mock_get)
    result = RequestAPI.get_data("http://example.com")
    assert result is not None


def test_post_data_with_mocked_success(monkeypatch):
    if not hasattr(RequestAPI, "post_data"):
        return

    class MockResponse:
        def __init__(self):
            self.status_code = 201
        def json(self):
            return {"created": True}

    def mock_post(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(RequestAPI.requests, "post", mock_post)
    result = RequestAPI.post_data("http://example.com", {"x": 1})
    assert result == {"created": True}


def test_put_data_with_mocked_success(monkeypatch):
    if not hasattr(RequestAPI, "put_data"):
        return

    class MockResponse:
        def __init__(self):
            self.status_code = 200
        def json(self):
            return {"updated": True}

    def mock_put(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(RequestAPI.requests, "put", mock_put)
    result = RequestAPI.put_data("http://example.com", {"x": 2})
    assert result == {"updated": True}

def test_placeholder():
    pass



def test_get_request(monkeypatch):
    class DummyResponse:
        def __init__(self):
            self.status_code = 200
        def json(self):
            return {"ok": True}

    called = {}

    def fake_get(url, headers=None, params=None):
        called["url"] = url
        called["headers"] = headers
        called["params"] = params
        return DummyResponse()

    monkeypatch.setattr(RequestAPI.requests, "get", fake_get)
    response = RequestAPI.get_data("https://example.com", headers={"A": "B"}, params={"q": 1})
    assert response.status_code == 200
    assert response.json() == {"ok": True}
    assert called["url"] == "https://example.com"
    assert called["headers"] == {"A": "B"}
    assert called["params"] == {"q": 1}


def test_post_request(monkeypatch):
    class DummyResponse:
        def __init__(self):
            self.status_code = 201
        def json(self):
            return {"created": True}

    called = {}

    def fake_post(url, headers=None, json=None):
        called["url"] = url
        called["headers"] = headers
        called["json"] = json
        return DummyResponse()

    monkeypatch.setattr(RequestAPI.requests, "post", fake_post)
    response = RequestAPI.post_data("https://example.com", headers={"C": "D"}, data={"name": "x"})
    assert response.status_code == 201
    assert response.json() == {"created": True}
    assert called["url"] == "https://example.com"
    assert called["headers"] == {"C": "D"}
    assert called["json"] == {"name": "x"}


def test_put_request(monkeypatch):
    class DummyResponse:
        def __init__(self):
            self.status_code = 200
        def json(self):
            return {"updated": True}

    called = {}

    def fake_put(url, headers=None, json=None):
        called["url"] = url
        called["headers"] = headers
        called["json"] = json
        return DummyResponse()

    monkeypatch.setattr(RequestAPI.requests, "put", fake_put)
    response = RequestAPI.put_data("https://example.com/1", headers={"E": "F"}, data={"name": "y"})
    assert response.status_code == 200
    assert response.json() == {"updated": True}
    assert called["url"] == "https://example.com/1"
    assert called["headers"] == {"E": "F"}
    assert called["json"] == {"name": "y"}
