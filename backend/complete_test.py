#!/usr/bin/env python3
"""
Complete test of the login and add-book flow
This script tests the exact same flow as the frontend
"""
import urllib.request
import urllib.parse
import urllib.error
import json
import base64
import sys
import socket

def test_complete_flow():
    print("=== Complete Flow Test ===")
    
    base_url = "http://localhost:8000"
    password = "123"  # From config.py
    
    # Step 0: Test server connectivity
    print("\n0. Testing server connectivity...")
    try:
        sock = socket.create_connection(("localhost", 8000), timeout=5)
        sock.close()
        print("✅ Server is reachable on port 8000")
    except Exception as e:
        print(f"❌ Server connection failed: {e}")
        return False
    
    # Step 1: Login
    print("\n1. Testing login...")
    auth_header = "Basic " + base64.b64encode(f":{password}".encode()).decode()
    
    login_req = urllib.request.Request(
        f"{base_url}/login",
        method="POST",
        headers={"Authorization": auth_header}
    )
    
    try:
        with urllib.request.urlopen(login_req) as response:
            if response.status == 200:
                login_data = json.loads(response.read().decode())
                token = login_data["token"]
                print(f"✅ Login successful!")
                print(f"   Token: {token}")
            else:
                print(f"❌ Login failed with status {response.status}")
                return False
    except urllib.error.HTTPError as e:
        error_response = e.read().decode()
        print(f"❌ Login failed with HTTP {e.code}: {error_response}")
        return False
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return False
    
    # Step 2: Add book (immediately after login)
    print("\n2. Testing add book...")
    book_data = {
        "ISBN": "123",
        "title": "Default Title", 
        "author": "Default Author",
        "year": 2025,
        "publisher": "Default Publisher",
        "cover": "http://example.com/default-cover.jpg",
        "gender": "Fiction",  # Note: backend expects "gender" field name
        "price": "19.99",
        "rating": "4.5"
    }
    
    print(f"   Book data: {book_data}")
    print(f"   Authorization header: Bearer {token}")
    
    add_book_req = urllib.request.Request(
        f"{base_url}/add-book",
        data=json.dumps(book_data).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(add_book_req, timeout=10) as response:
            if response.status == 200:
                add_book_data = json.loads(response.read().decode())
                print(f"✅ Add book successful!")
                print(f"   Response: {add_book_data}")
                return True
            else:
                print(f"❌ Add book failed with status {response.status}")
                return False
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode()
        print(f"❌ Add book failed with HTTP {e.code}: {error_msg}")
        return False
    except Exception as e:
        print(f"❌ Add book failed: {e}")
        return False

if __name__ == "__main__":
    success = test_complete_flow()
    if success:
        print("\n🎉 All tests passed! The backend is working correctly.")
    else:
        print("\n💥 Tests failed. Check the backend logs for more details.")
        sys.exit(1)
