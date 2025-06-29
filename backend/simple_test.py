import requests
import json

print("Testing backend connection...")

try:
    # Test server connection
    response = requests.get("http://localhost:8000")
    print(f"Server connection: {response.status_code}")
    
    # Test login
    login_data = {"username": "user", "password": "pass"}
    login_response = requests.post("http://localhost:8000/login", json=login_data)
    print(f"Login response: {login_response.status_code}")
    print(f"Login body: {login_response.text}")
    
    if login_response.status_code == 200:
        data = login_response.json()
        token = data.get("token")
        print(f"Got token: {token}")
        
        # Test add book with token
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "publication_year": 2023,
            "isbn": "1234567890123",
            "page_count": 300,
            "cover_url": "",
            "language": "en"
        }
        
        headers = {"Authorization": f"Bearer {token}"}
        book_response = requests.post("http://localhost:8000/add-book", json=book_data, headers=headers)
        print(f"Add book response: {book_response.status_code}")
        print(f"Add book body: {book_response.text}")
        
except Exception as e:
    print(f"Error: {e}")
