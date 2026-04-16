import pytest


class DummyResponse:
    def __init__(self, status_code, payload=None):
        self.status_code = status_code
        self._payload = payload if payload is not None else {}

    def json(self):
        return self._payload


class DummySession:
    def __init__(self):
        self.get_calls = []
        self.post_calls = []
        self.put_calls = []
        self.delete_calls = []
        self.get_responses = []
        self.post_response = None
        self.put_response = None
        self.delete_response = None

    def get(self, url, headers=None, params=None, timeout=None):
        self.get_calls.append(
            {"url": url, "headers": headers, "params": params, "timeout": timeout}
        )
        return self.get_responses.pop(0)

    def post(self, url, json=None, headers=None, timeout=None):
        self.post_calls.append(
            {"url": url, "json": json, "headers": headers, "timeout": timeout}
        )
        return self.post_response

    def put(self, url, json=None, headers=None, timeout=None):
        self.put_calls.append(
            {"url": url, "json": json, "headers": headers, "timeout": timeout}
        )
        return self.put_response

    def delete(self, url, headers=None, timeout=None):
        self.delete_calls.append(
            {"url": url, "headers": headers, "timeout": timeout}
        )
        return self.delete_response


def test_init_sets_attributes_and_session(monkeypatch):
    import src.complex_api_module as mod

    created = []

    class FakeRequests:
        @staticmethod
        def Session():
            session = DummySession()
            created.append(session)
            return session

    monkeypatch.setattr(mod, "requests", FakeRequests)

    client = mod.APIClient(token="abc", retries=5, timeout=9)

    assert client.token == "abc"
    assert client.retries == 5
    assert client.timeout == 9
    assert client.session is created[0]


def test_headers_without_token():
    import src.complex_api_module as mod

    client = mod.APIClient()
    headers = client._headers()

    assert headers == {"Accept": "application/json"}


def test_headers_with_token():
    import src.complex_api_module as mod

    client = mod.APIClient(token="secret")
    headers = client._headers()

    assert headers == {
        "Accept": "application/json",
        "Authorization": "Bearer secret",
    }


def test_get_user_success_without_details(monkeypatch):
    import src.complex_api_module as mod

    session = DummySession()
    session.get_responses = [DummyResponse(200, {"id": 7, "name": "Alice"})]

    class FakeRequests:
        @staticmethod
        def Session():
            return session

    monkeypatch.setattr(mod, "requests", FakeRequests)

    client = mod.APIClient(token="tok", retries=2, timeout=4)
    result = client.get_user(7)

    assert result == {"id": 7, "name": "Alice"}
    assert session.get_calls == [
        {
            "url": "https://api.example.com/users/7",
            "headers": {
                "Accept": "application/json",
                "Authorization": "Bearer tok",
            },
            "params": {},
            "timeout": 4,
        }
    ]


def test_get_user_success_with_details_after_retry(monkeypatch):
    import src.complex_api_module as mod

    session = DummySession()
    session.get_responses = [
        DummyResponse(500, {"error": "temporary"}),
        DummyResponse(200, {"id": 3, "details": True}),
    ]
    sleeps = []

    class FakeRequests:
        @staticmethod
        def Session():
            return session

    monkeypatch.setattr(mod, "requests", FakeRequests)
    monkeypatch.setattr(mod.time, "sleep", lambda value: sleeps.append(value))

    client = mod.APIClient(retries=2, timeout=6)
    result = client.get_user(3, include_details=True)

    assert result == {"id": 3, "details": True}
    assert len(session.get_calls) == 2
    assert session.get_calls[0]["params"] == {"details": "1"}
    assert session.get_calls[1]["params"] == {"details": "1"}
    assert sleeps == [0.1]


def test_get_user_raises_after_all_retries(monkeypatch):
    import src.complex_api_module as mod

    session = DummySession()
    session.get_responses = [
        DummyResponse(500),
        DummyResponse(404),
        DummyResponse(503),
    ]
    sleeps = []

    class FakeRequests:
        @staticmethod
        def Session():
            return session

    monkeypatch.setattr(mod, "requests", FakeRequests)
    monkeypatch.setattr(mod.time, "sleep", lambda value: sleeps.append(value))

    client = mod.APIClient(retries=3)

    with pytest.raises(Exception, match="Failed to fetch user"):
        client.get_user(99)

    assert len(session.get_calls) == 3
    assert sleeps == [0.1, 0.1, 0.1]


def test_create_user_success(monkeypatch):
    import src.complex_api_module as mod

    session = DummySession()
    session.post_response = DummyResponse(201, {"id": 1, "name": "Bob"})

    class FakeRequests:
        @staticmethod
        def Session():
            return session

    monkeypatch.setattr(mod, "requests", FakeRequests)

    client = mod.APIClient(token="t1", timeout=8)
    result = client.create_user("Bob", "bob@example.com")

    assert result == {"id": 1, "name": "Bob"}
    assert session.post_calls == [
        {
            "url": "https://api.example.com/users",
            "json": {"name": "Bob", "email": "bob@example.com"},
            "headers": {
                "Accept": "application/json",
                "Authorization": "Bearer t1",
            },
            "timeout": 8,
        }
    ]


def test_create_user_failure_raises(monkeypatch):
    import src.complex_api_module as mod

    session = DummySession()
    session.post_response = DummyResponse(400, {"error": "bad request"})

    class FakeRequests:
        @staticmethod
        def Session():
            return session

    monkeypatch.setattr(mod, "requests", FakeRequests)

    client = mod.APIClient()

    with pytest.raises(Exception, match="Failed to create user"):
        client.create_user("Bob", "bob@example.com")


def test_update_email_success(monkeypatch):
    import src.complex_api_module as mod

    session = DummySession()
    session.put_response = DummyResponse(200, {"updated": True})

    class FakeRequests:
        @staticmethod
        def Session():
            return session

    monkeypatch.setattr(mod, "requests", FakeRequests)

    client = mod.APIClient(timeout=10)
    result = client.update_email(5, "new@example.com")

    assert result == {"updated": True}
    assert session.put_calls == [
        {
            "url": "https://api.example.com/users/5/email",
            "json": {"email": "new@example.com"},
            "headers": {"Accept": "application/json"},
            "timeout": 10,
        }
    ]


def test_update_email_failure_raises(monkeypatch):
    import src.complex_api_module as mod

    session = DummySession()
    session.put_response = DummyResponse(500)

    class FakeRequests:
        @staticmethod
        def Session():
            return session

    monkeypatch.setattr(mod, "requests", FakeRequests)

    client = mod.APIClient()

    with pytest.raises(Exception, match="Failed to update email"):
        client.update_email(5, "new@example.com")


def test_delete_user_success(monkeypatch):
    import src.complex_api_module as mod

    session = DummySession()
    session.delete_response = DummyResponse(204)

    class FakeRequests:
        @staticmethod
        def Session():
            return session

    monkeypatch.setattr(mod, "requests", FakeRequests)

    client = mod.APIClient(token="del-token", timeout=2)
    result = client.delete_user(11)

    assert result is True
    assert session.delete_calls == [
        {
            "url": "https://api.example.com/users/11",
            "headers": {
                "Accept": "application/json",
                "Authorization": "Bearer del-token",
            },
            "timeout": 2,
        }
    ]


def test_delete_user_failure_raises(monkeypatch):
    import src.complex_api_module as mod

    session = DummySession()
    session.delete_response = DummyResponse(200)

    class FakeRequests:
        @staticmethod
        def Session():
            return session

    monkeypatch.setattr(mod, "requests", FakeRequests)

    client = mod.APIClient()

    with pytest.raises(Exception, match="Failed to delete user"):
        client.delete_user(11)


def test_list_users_success_with_next_page(monkeypatch):
    import src.complex_api_module as mod

    session = DummySession()
    session.get_responses = [
        DummyResponse(200, {"users": [{"id": 1}, {"id": 2}], "next_page": 3})
    ]

    class FakeRequests:
        @staticmethod
        def Session():
            return session

    monkeypatch.setattr(mod, "requests", FakeRequests)

    client = mod.APIClient(timeout=7)
    users, next_page = client.list_users(page=2)

    assert users == [{"id": 1}, {"id": 2}]
    assert next_page == 3
    assert session.get_calls == [
        {
            "url": "https://api.example.com/users",
            "headers": {"Accept": "application/json"},
            "params": {"page": 2},
            "timeout": 7,
        }
    ]


def test_list_users_success_defaults_to_empty_list_when_missing_users(monkeypatch):
    import src.complex_api_module as mod

    session = DummySession()
    session.get_responses = [DummyResponse(200, {"next_page": None})]

    class FakeRequests:
        @staticmethod
        def Session():
            return session

    monkeypatch.setattr(mod, "requests", FakeRequests)

    client = mod.APIClient()
    users, next_page = client.list_users()

    assert users == []
    assert next_page is None
    assert session.get_calls[0]["params"] == {"page": 1}


def test_list_users_failure_raises(monkeypatch):
    import src.complex_api_module as mod

    session = DummySession()
    session.get_responses = [DummyResponse(500)]

    class FakeRequests:
        @staticmethod
        def Session():
            return session

    monkeypatch.setattr(mod, "requests", FakeRequests)

    client = mod.APIClient()

    with pytest.raises(Exception, match="Failed to list users"):
        client.list_users(page=4)
