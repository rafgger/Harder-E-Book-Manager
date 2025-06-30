#!/usr/bin/env python3
"""
Quick diagnostic test for the backend server
"""
import requests
import json

def test_server():
    print("=== Quick Diagnostic Test ===")
    
    base_url = "http://localhost:8000"
    
    # Test 1: Basic connectivity
    print("\n1. Testing basic connectivity...")
    try:
        response = requests.get(f"{base_url}/docs", timeout=5)
        print(f"✅ Server responded with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Server connection failed: {e}")
        return False
    
    # Test 2: Login endpoint
    print("\n2. Testing login endpoint...")
    try:
        response = requests.post(
            f"{base_url}/login",
            auth=("", "123"),  # username is empty, password is "123"
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            token = data["token"]
            print(f"✅ Login successful! Token: {token}")
        else:
            print(f"❌ Login failed with status {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return False
    
    # Test 3: Add book with all required fields
    print("\n3. Testing add book...")
    book_data = {
        "ISBN": "diagnostic-123",
        "title": "Diagnostic Test Book",
        "author": "Test Author",
        "year": 2025,
        "publisher": "Test Publisher",
        "cover": "http://example.com/cover.jpg",
        "genre": "Fiction",  # Note: backend expects "genre" not "genre"
        "price": "19.99",
        "rating": "4.5"
    }
    
    try:
        response = requests.post(
            f"{base_url}/add-book",
            json=book_data,
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
        if response.status_code == 200:
            print(f"✅ Add book successful! Response: {response.json()}")
            return True
        else:
            print(f"❌ Add book failed with status {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Add book failed: {e}")
        return False

if __name__ == "__main__":
    success = test_server()
    if success:
        print("\n🎉 All diagnostic tests passed!")
    else:
        print("\n💥 Diagnostic tests failed!")
