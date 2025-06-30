#!/usr/bin/env python3
"""
Simple test for add-book endpoint
"""
import requests
import json

def test_add_book():
    print("=== Simple Add-Book Test ===")
    
    base_url = "http://localhost:8000"
    
    try:
        # Step 1: Login
        print("\n1. Logging in...")
        login_response = requests.post(f"{base_url}/login", auth=("", "123"), timeout=10)
        
        if login_response.status_code != 200:
            print(f"❌ Login failed: {login_response.status_code} - {login_response.text}")
            return False
            
        token = login_response.json()["token"]
        print(f"✅ Login successful, token: {token}")
        
        # Step 2: Add book
        print("\n2. Adding book...")
        book_data = {
            "ISBN": "simple-test-456",
            "title": "Simple Test Book",
            "author": "Simple Author", 
            "year": 2025,
            "publisher": "Simple Publisher",
            "cover": "http://example.com/simple.jpg",
            "gender": "Non-Fiction",
            "price": "15.99",
            "rating": "3.8"
        }
        
        headers = {"Authorization": f"Bearer {token}"}
        add_response = requests.post(f"{base_url}/add-book", json=book_data, headers=headers, timeout=10)
        
        print(f"Add-book status: {add_response.status_code}")
        print(f"Add-book response: {add_response.text}")
        
        if add_response.status_code == 200:
            print("✅ Add-book successful!")
            return True
        else:
            print("❌ Add-book failed!")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        return False

if __name__ == "__main__":
    success = test_add_book()
    if success:
        print("\n🎉 Simple test passed!")
    else:
        print("\n💥 Simple test failed!")
