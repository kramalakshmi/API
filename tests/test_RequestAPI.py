
import pytest
from unittest.mock import patch
import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import  RequestAPI 
#import get_request, post_request, put_request, delete_request  # Replace 'your_module' with the actual module name

class TestAPIRequests:

    @patch('requests.get')
    def test_get_request_success(self, mock_get):
        # Arrange
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"id": 1, "name": "John Doe"}]

        # Act
        get_request()

        # Assert
        mock_get.assert_called_once()

    @patch('requests.post')
    def test_post_request_success(self, mock_post):
        # Arrange
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {"id": 123, "name": "Naveena"}

        # Act
        user_id = post_request()

        # Assert
        assert user_id == 123
        mock_post.assert_called_once()

    @patch('requests.put')
    def test_put_request_success(self, mock_put):
        # Arrange
        mock_put.return_value.status_code = 200
        mock_put.return_value.json.return_value = {"id": 123, "name": "Naveena", "status": "inactive"}

        # Act
        put_request(123)

        # Assert
        mock_put.assert_called_once_with(
            "https://gorest.co.in/public/v2/users/123",
            json={"name": "Naveena", "email": "naveena@aa.com", "gender": "male", "status": "inactive"},
            headers={"Authorization": "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"}
        )

    @patch('requests.delete')
    def test_delete_request_success(self, mock_delete):
        # Arrange
        mock_delete.return_value.status_code = 204

        # Act
        delete_request(123)

        # Assert
        mock_delete.assert_called_once_with(
            "https://gorest.co.in/public/v2/users/123",
            headers={"Authorization": "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"}
        )
