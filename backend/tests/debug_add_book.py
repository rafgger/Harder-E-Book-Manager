#!/usr/bin/env python3
"""
Debug script to isolate the add-book 500 error
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import json
import time

def debug_add_book():
    print("=== Debug Add Book 500 Error ===")
    
    base_url = "http://localhost:8000"
    password = "123"
    
    # Step 1: Login
    print("\n1. Testing login...")
    try:
        response = requests.post(f"{base_url}/login", auth=("user", password))
        if response.status_code == 200:
            token = response.json()["token"]
            print(f"✓ Login successful, token: {token[:20]}...")
        else:
            print(f"✗ Login failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Login error: {e}")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Step 2: Test adding a simple book
    print("\n2. Testing book addition...")
    
    # Use unique timestamp-based ISBN
    import time
    timestamp = str(int(time.time()))
    
    test_book = {
        "ISBN": f"debug-book-{timestamp}",
        "title": "Debug Test Book",
        "author": "Test Author",
        "year": 2025,
        "publisher": "Debug Publisher",
        "cover": "http://example.com/debug.jpg",
        "genre": "Fiction",
        "price": "19.99",
        "rating": "4.5"
    }
    
    print(f"   Adding book with ISBN: {test_book['ISBN']}")
    print(f"   Book data: {json.dumps(test_book, indent=2)}")
    
    try:
        response = requests.post(f"{base_url}/add-book", json=test_book, headers=headers)
        print(f"   Response status: {response.status_code}")
        print(f"   Response headers: {dict(response.headers)}")
        print(f"   Response text: {response.text}")
        
        if response.status_code == 200:
            print("✓ Book addition successful!")
            result = response.json()
            print(f"   Response data: {result}")
            return True
        else:
            print(f"✗ Book addition failed with status {response.status_code}")
            print(f"   Error details: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Book addition error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_add_book()
