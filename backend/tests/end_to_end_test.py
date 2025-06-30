#!/usr/bin/env python3
"""
End-to-end test to debug the login and add-book flow
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_login():
    """Test login and get a session token"""
    print("=== Testing Login ===")
    
    try:
        # Use HTTP Basic Auth as expected by the backend
        response = requests.post(f"{BASE_URL}/login", auth=("user", "123"))
        print(f"Login status: {response.status_code}")
        print(f"Login response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("token")
            print(f"Received token: {token}")
            return token
        else:
            print(f"Login failed with status {response.status_code}")
            return None
    except Exception as e:
        print(f"Login error: {e}")
        return None

def test_add_book(token):
    """Test adding a book with the session token"""
    print("\n=== Testing Add Book ===")
    
    if not token:
        print("No token available for add-book test")
        return False
    
    book_data = {
        "ISBN": "1234567890123",
        "title": "Test Book",
        "author": "Test Author", 
        "year": 2023,
        "publisher": "Test Publisher",
        "cover": "http://example.com/default-cover.jpg"
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    print(f"Using headers: {headers}")
    print(f"Sending book data: {book_data}")
    
    try:
        response = requests.post(f"{BASE_URL}/add-book", json=book_data, headers=headers)
        print(f"Add-book status: {response.status_code}")
        print(f"Add-book response: {response.text}")
        
        if response.status_code == 200:
            print("Book added successfully!")
            return True
        else:
            print(f"Add-book failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Add-book error: {e}")
        return False

def test_get_books(token):
    """Test getting books list"""
    print("\n=== Testing Get Books ===")
    
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    
    try:
        response = requests.get(f"{BASE_URL}/books", headers=headers)
        print(f"Get books status: {response.status_code}")
        print(f"Get books response: {response.text}")
        
        if response.status_code == 200:
            books = response.json()
            print(f"Found {len(books)} books")
            return True
        else:
            print(f"Get books failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Get books error: {e}")
        return False

def main():
    print("Starting end-to-end test...")
    
    # Test if server is running
    try:
        response = requests.get(BASE_URL)
        print(f"Server status: {response.status_code}")
    except Exception as e:
        print(f"Server not reachable: {e}")
        print("Please make sure the backend server is running on port 8000")
        return
    
    # Test login
    token = test_login()
    
    if token:
        # Test add book
        add_success = test_add_book(token)
        
        # Test get books
        get_success = test_get_books(token)
        
        print(f"\n=== Test Results ===")
        print(f"Login: {'✓' if token else '✗'}")
        print(f"Add Book: {'✓' if add_success else '✗'}")
        print(f"Get Books: {'✓' if get_success else '✗'}")
    else:
        print("\nCannot proceed with other tests without a valid token")

if __name__ == "__main__":
    main()
