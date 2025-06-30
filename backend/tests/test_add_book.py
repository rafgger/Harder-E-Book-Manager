import requests

BASE_URL = "http://localhost:8000"
PASSWORD = "<your_password>"  # Replace with your actual password

# 1. Login to get a session token
def get_token():
    resp = requests.post(f"{BASE_URL}/login", auth=("", PASSWORD))
    resp.raise_for_status()
    return resp.json()["token"]

# 2. Add a book using the token
def add_book(token):
    book = {
        "ISBN": "testmanual",
        "title": "Manual Test Book",
        "author": "Manual Author",
        "year": 2025,
        "publisher": "Manual Publisher",
        "cover": "http://example.com/manual.jpg"
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    resp = requests.post(f"{BASE_URL}/add-book", json=book, headers=headers)
    print("Add book status:", resp.status_code)
    print("Response:", resp.text)
    resp.raise_for_status()

if __name__ == "__main__":
    token = get_token()
    print("Token:", token)
    add_book(token)
