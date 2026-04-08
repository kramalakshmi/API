To create unit tests for the provided code using `pytest`, we will mock the HTTP requests made by the `requests` library. This allows us to test the logic of our functions without making actual HTTP calls. We'll use the `pytest` and `unittest.mock` modules to accomplish this.

Make sure you have `pytest` and `requests` installed in your environment. You can run the command `pip install pytest requests` to install them if you haven't done so. 

Here's how we can write the tests:

```python
import pytest
from unittest.mock import patch, Mock
import requests
from your_module import get_request, post_request, put_request, delete_request

# Test GET Request
@patch('requests.get')
def test_get_request(mock_get):
    # Mock the response data
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{'id': 1, 'name': 'User1'}, {'id': 2, 'name': 'User2'}]
    mock_get.return_value = mock_response

    # Call the function
    get_request()

    # Assert that the requests.get was called once
    mock_get.assert_called_once()


# Test POST Request
@patch('requests.post')
def test_post_request(mock_post):
    # Mock the response data
    mock_response = Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = {'id': 3, 'name': 'Naveena', 'email': 'naveena@aa.com'}
    mock_post.return_value = mock_response

    # Call the function
    user_id = post_request()

    # Assert that the requests.post was called once
    mock_post.assert_called_once()
    # Assert user id is what we mocked
    assert user_id == 3


# Test PUT Request
@patch('requests.put')
def test_put_request(mock_put):
    # Prepare a user_id for testing
    user_id = 3
    
    # Mock the response data
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'id': user_id, 'status': 'inactive'}
    mock_put.return_value = mock_response

    # Call the function
    put_request(user_id)

    # Assert that the requests.put was called with the correct URL
    mock_put.assert_called_once_with(f"https://gorest.co.in/public/v2/users/{user_id}", json={
        "name": "Naveena",
        "email": "naveena@aa.com",
        "gender": "male",
        "status": "inactive"
    }, headers={"Authorization": "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"})


# Test DELETE Request
@patch('requests.delete')
def test_delete_request(mock_delete):
    # Prepare a user_id for testing
    user_id = 3
    
    # Mock the response data
    mock_response = Mock()
    mock_response.status_code = 204
    mock_delete.return_value = mock_response

    # Call the function
    delete_request(user_id)

    # Assert that the requests.delete was called with the correct URL
    mock_delete.assert_called_once_with(f"https://gorest.co.in/public/v2/users/{user_id}", headers={"Authorization": "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"})

# To run the tests, you would typically run `pytest` from the command line in the directory containing this test script.
```

### Breakdown of the Test Cases:

1. **Test GET Request:**
   - Mocks the `requests.get` method and simulates a successful response.
   - Asserts that `requests.get()` was called exactly once.

2. **Test POST Request:**
   - Mocks `requests.post` to return a successful response with a mock user ID.
   - Asserts that the returned user ID matches the mock data.

3. **Test PUT Request:**
   - Mocks `requests.put` and simulates a successful update response.
   - Asserts that `requests.put()` was called with the correct URL and JSON data.

4. **Test DELETE Request:**
   - Mocks `requests.delete` and simulates a successful deletion.
   - Asserts that `requests.delete()` was called with the correct URL.

### How to Run the Tests:
To execute the tests, save this testing code in a file, for example `test_api.py`, and run:
```bash
pytest test_api.py
```

This will run all the defined test cases and report their outcomes, ensuring that your API function logic behaves as expected.