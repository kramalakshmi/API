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


def test_placeholder():
    pass
