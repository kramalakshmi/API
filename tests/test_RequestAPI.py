To create unit tests for the provided code using `pytest`, we'll utilize the `responses` library, which allows us to mock HTTP requests made by the `requests` library without actually hitting the API. This way, we can simulate various responses and test the functions independently.

Below are test cases that cover the following scenarios:

1. Successful GET request.
2. Successful POST request.
3. Successful PUT request.
4. Successful DELETE request.
5. Edge cases for each request (like unauthorized access, not found, etc.).

First, ensure you have installed the required packages:
```bash
pip install pytest responses
```

Now, here is the `test_api.py` file with the unit tests:

```python
import pytest
import responses
import json
from your_module import get_request, post_request, put_request, delete_request

BASE_URL = "https://gorest.co.in"
AUTH_TOKEN = "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"
HEADERS = {"Authorization": AUTH_TOKEN}

@pytest.fixture(autouse=True)
def mock_requests():
    with responses.RequestsMock() as rsps:
        yield rsps

def test_get_request(mock_requests):
    url = f"{BASE_URL}/public/v2/users"
    mock_requests.add(responses.GET, url, json=[{"id": 1, "name": "John Doe"}], status=200)

    # Call the function
    get_request()

    # Verify the request
    assert len(mock_requests.calls) == 1
    assert mock_requests.calls[0].request.url == url

def test_post_request(mock_requests):
    url = f"{BASE_URL}/public/v2/users"
    response_data = {"id": 1, "name": "Naveena"}
    mock_requests.add(responses.POST, url, json=response_data, status=201)

    # Call the function
    user_id = post_request()

    # Verify the result
    assert user_id == 1
    assert len(mock_requests.calls) == 1
    assert mock_requests.calls[0].request.url == url

def test_put_request(mock_requests):
    user_id = 1
    url = f"{BASE_URL}/public/v2/users/{user_id}"
    mock_requests.add(responses.PUT, url, json={"id": user_id, "status": "inactive"}, status=200)

    # Call the function
    put_request(user_id)

    # Verify the request
    assert len(mock_requests.calls) == 1
    assert mock_requests.calls[0].request.url == url

def test_delete_request(mock_requests):
    user_id = 1
    url = f"{BASE_URL}/public/v2/users/{user_id}"
    mock_requests.add(responses.DELETE, url, status=204)

    # Call the function
    delete_request(user_id)

    # Verify the request
    assert len(mock_requests.calls) == 1
    assert mock_requests.calls[0].request.url == url

def test_get_request_not_found(mock_requests):
    url = f"{BASE_URL}/public/v2/users"
    mock_requests.add(responses.GET, url, json={"message": "Not Found"}, status=404)

    # Execute and observe the handling
    with pytest.raises(Exception):
        get_request()  # You might want to modify get_request to raise an error on non-200 status.

def test_post_request_bad_request(mock_requests):
    url = f"{BASE_URL}/public/v2/users"
    mock_requests.add(responses.POST, url, json={"message": "Bad Request"}, status=400)

    # Execute and catch the handling
    with pytest.raises(Exception):
        user_id = post_request()  # You might need to modify post_request to handle non-201 status.

# You can further add tests for other scenarios like unauthorized access.
```

### Important Notes:
1. **Request Handling**: The original code does not handle exceptions (e.g., when a request fails). To run these tests successfully, consider updating `get_request`, `post_request`, and similar functions to raise exceptions or return error messages on unexpected HTTP status codes. This way, tests like `test_get_request_not_found` and `test_post_request_bad_request` will work correctly.
  
2. **Import Path**: Replace `from your_module import ...` with the actual path where your functions are defined.

3. **Deterministic Tests**: Each test simulates a specific scenario with expected results, ensuring consistent and reliable outputs each time tests are run. 

4. **Running Tests**: You can run your tests using the command:
   ```bash
   pytest test_api.py
   ``` 

This setup covers testing of various HTTP methods and ensures that the functionality is validated without making real API calls.