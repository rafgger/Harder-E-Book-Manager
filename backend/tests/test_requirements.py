#!/usr/bin/env python3
"""
Simple test to check add-book endpoint requirements
"""
import requests
import json

def test_add_book_requirements():
    print("=== Add Book Requirements Test ===")
    
    base_url = "http://localhost:8000"
    
    # Step 1: Get a fresh token
    print("\n1. Getting fresh token...")
    try:
        login_response = requests.post(f"{base_url}/login", auth=("user", "123"))
        if login_response.status_code != 200:
            print(f"❌ Login failed: {login_response.status_code}")
            return False
        
        token = login_response.json()["token"]
        print(f"✅ Got token: {token[:20]}...")
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Step 2: Test with missing fields to see what's required
    print("\n2. Testing field requirements...")
    
    minimal_book = {
        "ISBN": "requirements-test-123",
        "title": "Requirements Test",
        "author": "Test Author",
        "year": 2025,
        "publisher": "Test Publisher",
        "cover": "http://example.com/cover.jpg"
    }
    
    try:
        response = requests.post(f"{base_url}/add-book", json=minimal_book, headers=headers)
        print(f"Minimal book response: {response.status_code}")
        print(f"Response text: {response.text}")
        
        if response.status_code == 400:
            print("✅ Field validation is working - missing fields detected")
        elif response.status_code == 500:
            print("❌ 500 error with minimal fields - backend issue")
        else:
            print(f"Unexpected status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Request error: {e}")
        return False
    
    # Step 3: Test with all fields
    print("\n3. Testing with all required fields...")
    
    complete_book = {
        "ISBN": "requirements-test-complete-456",
        "title": "Complete Requirements Test",
        "author": "Test Author",
        "year": 2025,
        "publisher": "Test Publisher", 
        "cover": "http://example.com/cover.jpg",
        "genre": "Fiction",
        "price": "19.99",
        "rating": "4.5"
    }
    
    try:
        response = requests.post(f"{base_url}/add-book", json=complete_book, headers=headers)
        print(f"Complete book response: {response.status_code}")
        print(f"Response text: {response.text}")
        
        if response.status_code == 200:
            print("✅ All fields accepted - book added successfully")
        elif response.status_code == 400:
            print("❌ Field validation failed even with all fields")
        elif response.status_code == 500:
            print("❌ 500 error with all fields - backend processing issue")
        else:
            print(f"Unexpected status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Request error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_add_book_requirements()
