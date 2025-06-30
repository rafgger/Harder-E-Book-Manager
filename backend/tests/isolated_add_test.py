#!/usr/bin/env python3
"""
Minimal test to isolate the add-book 500 error
"""
import requests
import json
import time

def test_add_book_isolated():
    print("=== Isolated Add Book Test ===")
    
    base_url = "http://localhost:8000"
    password = "123"
    
    # Step 1: Login
    print("1. Logging in...")
    try:
        response = requests.post(f"{base_url}/login", auth=("user", password))
        if response.status_code != 200:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return False
        
        token = response.json()["token"]
        print(f"✅ Login successful")
        
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Step 2: Add a very simple book
    print("\n2. Adding a minimal test book...")
    
    timestamp = int(time.time())
    test_book = {
        "ISBN": f"isolated-test-{timestamp}",
        "title": "Isolated Test Book",
        "author": "Test Author",
        "year": 2025,
        "publisher": "Test Publisher",
        "cover": "http://example.com/test.jpg",
        "genre": "Fiction",
        "price": "19.99",
        "rating": "4.5"
    }
    
    print(f"Book data: {json.dumps(test_book, indent=2)}")
    
    try:
        print("Sending POST request...")
        response = requests.post(
            f"{base_url}/add-book", 
            json=test_book, 
            headers=headers,
            timeout=10
        )
        
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        print(f"Response text: {response.text}")
        
        if response.status_code == 200:
            print("✅ Book added successfully!")
            return True
        else:
            print(f"❌ Book addition failed")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out - server might be hanging")
        return False
    except Exception as e:
        print(f"❌ Request error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_add_book_isolated()
    if success:
        print("\n🎉 Test completed successfully!")
    else:
        print("\n💥 Test failed!")
