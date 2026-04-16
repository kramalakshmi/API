import requests
import time

BASE_URL = "https://api.example.com"

class APIClient:
    def __init__(self, token=None, retries=2, timeout=3):
        self.session = requests.Session()
        self.token = token
        self.retries = retries
        self.timeout = timeout

    def _headers(self):
        headers = {"Accept": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def get_user(self, user_id, include_details=False):
        url = f"{BASE_URL}/users/{user_id}"
        params = {"details": "1"} if include_details else {}
        for _ in range(self.retries):
            response = self.session.get(url, headers=self._headers(), params=params, timeout=self.timeout)
            if response.status_code == 200:
                return response.json()
            time.sleep(0.1)
        raise Exception("Failed to fetch user")

    def create_user(self, name, email):
        url = f"{BASE_URL}/users"
        payload = {"name": name, "email": email}
        response = self.session.post(url, json=payload, headers=self._headers(), timeout=self.timeout)
        if response.status_code != 201:
            raise Exception("Failed to create user")
        return response.json()

    def update_email(self, user_id, new_email):
        url = f"{BASE_URL}/users/{user_id}/email"
        payload = {"email": new_email}
        response = self.session.put(url, json=payload, headers=self._headers(), timeout=self.timeout)
        if response.status_code != 200:
            raise Exception("Failed to update email")
        return response.json()

    def delete_user(self, user_id):
        url = f"{BASE_URL}/users/{user_id}"
        response = self.session.delete(url, headers=self._headers(), timeout=self.timeout)
        if response.status_code != 204:
            raise Exception("Failed to delete user")
        return True

    def list_users(self, page=1):
        url = f"{BASE_URL}/users"
        response = self.session.get(url, headers=self._headers(), params={"page": page}, timeout=self.timeout)
        if response.status_code != 200:
            raise Exception("Failed to list users")
        data = response.json()
        return data.get("users", []), data.get("next_page")