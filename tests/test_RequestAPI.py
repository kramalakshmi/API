import pytest
import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import RequestAPI


class DummyResponse:
    def __init__(self, data):
        self._data = data

    def json(self):
        return self._data


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