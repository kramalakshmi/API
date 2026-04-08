
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
```

### Explanation of the Tests:
1. **test_get_data**: This test checks whether `get_data` correctly retrieves data by mocking a GET request to the provided URL. It verifies that the returned JSON matches the expected structure and data.

2. **test_post_data**: This test checks if `post_data` correctly handles a POST request. It sends a payload and checks that the returned response matches the expected output.

3. **test_put_data**: This test verifies that `put_data` correctly updates an existing resource via a PUT request and checks if the returned response aligns with what we expect.

### Notes:
- Adjust the expected responses in the tests to reflect the real API responses if you're not actually using the JSONPlaceholder API.
- Replace `from your_module import ...` with the actual module name where your functions are defined. 
- You may want to install `requests-mock` if not already done, as it is critical for mocking the requests effectively. 

To run the tests, save the test code to a file (for example, `test_your_module.py`) and execute it using:

```bash
pytest test_your_module.py
``` 

This will execute the tests and report results, ensuring your functions work as intended without making real API calls.
