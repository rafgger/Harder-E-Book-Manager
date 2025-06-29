#!/usr/bin/env python3
"""
Test script that mimics the frontend login and add-book behavior
"""
import urllib.request
import urllib.parse
import urllib.error
import json
import base64

def test_frontend_behavior():
    print("=== Testing Frontend Behavior ===")
    
    base_url = "http://localhost:8000"
    
    # Step 1: Login (like the frontend does)
    print("\n1. Testing login...")
    password = "123"  # From config.py
    auth_header = "Basic " + base64.b64encode(f":{password}".encode()).decode()
    
    login_req = urllib.request.Request(
        f"{base_url}/login",
        method="POST",
        headers={"Authorization": auth_header}
    )
    
    try:
        with urllib.request.urlopen(login_req) as response:
            login_data = json.loads(response.read().decode())
            token = login_data["token"]
            print(f"✅ Login successful, token: {token}")
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return
    
    # Step 2: Add book (like the frontend does)
    print("\n2. Testing add book...")
    book_data = {
        "ISBN": "123",
        "title": "Default Title",
        "author": "Default Author",
        "year": 2025,
        "publisher": "Default Publisher",
        "cover": "http://example.com/default-cover.jpg"
    }
    
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
        with urllib.request.urlopen(add_book_req) as response:
            add_book_data = json.loads(response.read().decode())
            print(f"✅ Add book successful: {add_book_data}")
    except urllib.error.HTTPError as e:
        print(f"❌ Add book failed with HTTP {e.code}: {e.read().decode()}")
    except Exception as e:
        print(f"❌ Add book failed: {e}")

if __name__ == "__main__":
    test_frontend_behavior()
