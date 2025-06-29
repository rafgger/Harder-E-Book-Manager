import requests
import json

# Test the authentication fix
BASE_URL = "http://localhost:8000"

print("=== Testing Authentication Fix ===")

# Step 1: Login
print("1. Testing login...")
try:
    response = requests.post(f"{BASE_URL}/login", auth=("user", "123"))
    print(f"Login status: {response.status_code}")
    if response.status_code == 200:
        token = response.json()["token"]
        print(f"Got token: {token}")
        
        # Step 2: Test add-book with Bearer token
        print("\n2. Testing add-book with Bearer token...")
        book_data = {
            "ISBN": "auth-test-123",
            "title": "Auth Test Book",
            "author": "Test Author",
            "year": 2025,
            "publisher": "Test Publisher",
            "cover": "http://example.com/cover.jpg"
        }
        
        headers = {"Authorization": f"Bearer {token}"}
        add_response = requests.post(f"{BASE_URL}/add-book", json=book_data, headers=headers)
        print(f"Add-book status: {add_response.status_code}")
        print(f"Add-book response: {add_response.text}")
        
        if add_response.status_code == 200:
            print("✅ SUCCESS: Authentication fix is working!")
        else:
            print("❌ FAILED: Authentication still not working")
            
    else:
        print("❌ Login failed")
        
except Exception as e:
    print(f"❌ Error: {e}")
