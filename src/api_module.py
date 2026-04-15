import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

def get_user(user_id):
    url = f"{BASE_URL}/users/{user_id}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch user")
    return response.json()

def create_post(user_id, title, body):
    url = f"{BASE_URL}/posts"
    payload = {"userId": user_id, "title": title, "body": body}
    response = requests.post(url, json=payload)
    if response.status_code != 201:
        raise Exception("Failed to create post")
    return response.json()

def update_post(post_id, title, body):
    url = f"{BASE_URL}/posts/{post_id}"
    payload = {"title": title, "body": body}
    response = requests.put(url, json=payload)
    if response.status_code != 200:
        raise Exception("Failed to update post")
    return response.json()

def delete_post(post_id):
    url = f"{BASE_URL}/posts/{post_id}"
    response = requests.delete(url)
    if response.status_code != 200:
        raise Exception("Failed to delete post")
    return True
