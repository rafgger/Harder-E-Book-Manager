import requests
import json

# Test the login and add-book flow
base_url = "http://localhost:8000"

def test_login_and_add_book():
    print("=== Testing Login ===")
    # Test login - use correct username:password (user:123)
    login_response = requests.post(
        f"{base_url}/login",
        auth=("user", "123")  # This is the correct way to do HTTP Basic Auth
    )
    print(f"Login status: {login_response.status_code}")
    if login_response.status_code == 200:
        token = login_response.json()["token"]
        print(f"Token received: {token}")
        
        print("\n=== Testing Add Book ===")
        # Test add book
        book_data = {
            "ISBN": "12223",
            "title": "Test Book",
            "author": "Test Author",
            "year": 2025,
            "publisher": "Test Publisher",
            "cover": "http://example.com/cover.jpg"
        }
        
        add_response = requests.post(
            f"{base_url}/add-book",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json=book_data
        )
        print(f"Add book status: {add_response.status_code}")
        print(f"Add book response: {add_response.text}")
    else:
        print(f"Login failed: {login_response.text}")

if __name__ == "__main__":
    test_login_and_add_book()
