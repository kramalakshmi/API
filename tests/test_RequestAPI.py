
import pytest
import requests
import requests_mock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import RequestAPI
from RequestAPI import get_data, post_data, put_data  # Adjust the import statement based on your actual module name.

def test_get_data():
    url = "https://jsonplaceholder.typicode.com/posts/1"
    expected_response = {
        "userId": 1,
        "id": 1,
        "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
        "body": "quia et suscipit\nsuscipit..."
    }

    with requests_mock.Mocker() as m:
        m.get(url, json=expected_response)
        response = get_data(url)
        assert response == expected_response

def test_post_data():
    url = "https://jsonplaceholder.typicode.com/posts"
    payload = {"title": "Test"}
    expected_response = {
        "id": 101,
        "title": "Test",
        # other fields as typically returned by the API
    }

    with requests_mock.Mocker() as m:
        m.post(url, json=expected_response)
        response = post_data(url, payload)
        assert response == expected_response

def test_put_data():
    url = "https://jsonplaceholder.typicode.com/posts/1"
    payload = {"title": "Updated"}
    expected_response = {
        "id": 1,
        "title": "Updated",
        # other fields as typically returned by the API
    }

    with requests_mock.Mocker() as m:
        m.put(url, json=expected_response)
        response = put_data(url, payload)
        assert response == expected_response
