import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import requests
import RequestAPI


class DummyResponse:
    def __init__(self, data):
        self.data = data

    def json(self):
        return self.data


def test_get_data(monkeypatch):
    expected = {"id": 1}

    def mock_get(url):
        return DummyResponse(expected)

    monkeypatch.setattr(requests, "get", mock_get)
    assert RequestAPI.get_data("http://example.com") == expected


def test_post_data(monkeypatch):
    expected = {"title": "Test"}

    def mock_post(url, json):
        return DummyResponse(expected)

    monkeypatch.setattr(requests, "post", mock_post)
    assert RequestAPI.post_data("http://example.com", {"title": "Test"}) == expected


def test_put_data(monkeypatch):
    expected = {"title": "Updated"}

    def mock_put(url, json):
        return DummyResponse(expected)

    monkeypatch.setattr(requests, "put", mock_put)
    assert RequestAPI.put_data("http://example.com", {"title": "Updated"}) == expected
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import pytest
import requests
from unittest.mock import Mock
import main as main_module
def test_main_prints_results(monkeypatch, capsys):
    get_mock = Mock()
    get_mock.json.return_value = {"id": 1}
    post_mock = Mock()
    post_mock.json.return_value = {"title": "Test"}
    put_mock = Mock()
    put_mock.json.return_value = {"title": "Updated"}
    monkeypatch.setattr(requests, "get", Mock(return_value=get_mock))
    monkeypatch.setattr(requests, "post", Mock(return_value=post_mock))
    monkeypatch.setattr(requests, "put", Mock(return_value=put_mock))
    main_module.main()
    captured = capsys.readouterr()
    lines = captured.out.strip().splitlines()
    assert lines == ["{'id': 1}", "{'title': 'Test'}", "{'title': 'Updated'}"]
