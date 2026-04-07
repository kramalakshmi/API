To test the provided code using `pytest`, we will create unit tests that cover the functionality of the `get_request`, `post_request`, `put_request`, and `delete_request` functions. Since these functions perform HTTP requests, we will use the `requests-mock` library to mock those requests and responses to ensure that our tests are deterministic and do not depend on external services.

Make sure to first install `pytest` and `requests-mock` if you haven't done this yet:

```bash
pip install pytest requests-mock
```

Below is the `pytest` code to test the provided functions:

```python
import pytest
import requests
import requests_mock
from your_module import get_request, post_request, put_request, delete_request

# Mocking the base URL and Auth token for tests
base_url = "https://gorest.co.in"
auth_token = "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"

def test_get_request():
    with requests_mock.Mocker() as m:
        m.get(f"{base_url}/public/v2/users", status_code=200, json=[{"id": 1, "name": "John Doe"}])
        response = get_request()
        assert response is None  # Currently there is no return value

def test_post_request():
    with requests_mock.Mocker() as m:
        m.post(f"{base_url}/public/v2/users", status_code=201, json={"id": 123, "name": "Naveena"})
        user_id = post_request()
        assert user_id == 123  # Ensure the returned user ID is correct

def test_put_request():
    user_id = 123
    with requests_mock.Mocker() as m:
        m.put(f"{base_url}/public/v2/users/{user_id}", status_code=200, json={"id": user_id, "status": "inactive"})
        response = put_request(user_id)
        assert response is None  # Currently there is no return value

def test_delete_request():
    user_id = 123
    with requests_mock.Mocker() as m:
        m.delete(f"{base_url}/public/v2/users/{user_id}", status_code=204)
        response = delete_request(user_id)
        assert response is None  # Currently there is no return value

if __name__ == "__main__":
    pytest.main()
```

### Explanation:
- **Mocking Responses:** The `requests_mock.Mocker()` is used to mock responses for different HTTP methods. We set the expected URL, status code, and the JSON response that should be returned by the mocked request.
- **Assertions:** We verify that the responses from the functions match our expectations, such as ensuring that the `user_id` returned by `post_request` is correct. Functions like `get_request`, `put_request`, and `delete_request` currently have no return values, but in a real-world scenario, we could modify them to return relevant information.
- **Test Structure:** We define a clear function for each HTTP method, keeping test cases isolated and focusing on one function at a time.

Make sure to replace `your_module` with the actual name of your Python file (without the `.py` extension) where you have the provided functions defined.

### Running Tests:
To run the tests, execute the following command in the terminal:

```bash
pytest your_test_file.py
```

This will run the tests and output the results, indicating if all tests have passed or if there were any failures.