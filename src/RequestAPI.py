import requests

def get_data(url):
    return requests.get(url).json()

def post_data(url, payload):
    return requests.post(url, json=payload).json()

def put_data(url, payload):
    return requests.put(url, json=payload).json()

if __name__ == "__main__":
    
    # Example usage
    print(get_data("https://jsonplaceholder.typicode.com/posts/1"))
    print(post_data("https://jsonplaceholder.typicode.com/posts", {"title": "Test"}))
    print(put_data("https://jsonplaceholder.typicode.com/posts/1", {"title": "Updated"}))
