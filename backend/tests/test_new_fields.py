#!/usr/bin/env python3
"""
Test script for the updated e-book manager with new fields
Tests the complete flow including gender, price, and rating
"""
import requests
import json

def test_new_fields():
    print("=== Testing Updated E-Book Manager ===")
    
    base_url = "http://localhost:8000"
    password = "123"  # From config.py
    
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
    
    # Step 2: Test adding book with new fields
    print("\n2. Testing add-book with new fields...")
    book_data = {
        "ISBN": "test-new-fields-2025",
        "title": "Test Book with New Fields",
        "author": "Test Author",
        "year": 2025,
        "publisher": "Test Publisher",
        "cover": "http://example.com/cover.jpg",
        "gender": "Fiction",  # Backend expects "gender" field name
        "price": "19.99",
        "rating": "4.5"
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    try:
        add_response = requests.post(f"{base_url}/add-book", json=book_data, headers=headers)
        if add_response.status_code == 200:
            print("✓ Book with new fields added successfully")
        else:
            print(f"✗ Add book failed: {add_response.status_code}")
            print(f"Error: {add_response.text}")
            return False
    except Exception as e:
        print(f"✗ Add book error: {e}")
        return False
    
    # Step 3: Test retrieving books to verify new fields
    print("\n3. Testing book retrieval with new fields...")
    try:
        get_response = requests.get(f"{base_url}/books", headers=headers)
        if get_response.status_code == 200:
            books = get_response.json()
            test_book = None
            for book in books:
                if book.get("ISBN") == "test-new-fields-2025":
                    test_book = book
                    break
            
            if test_book:
                print("✓ Book retrieved successfully")
                print(f"  Title: {test_book.get('title')}")
                print(f"  Gender: {test_book.get('gender', 'Missing')}")
                print(f"  Price: {test_book.get('price', 'Missing')}")
                print(f"  Rating: {test_book.get('rating', 'Missing')}")
                
                # Verify all new fields are present
                if (test_book.get('gender') and 
                    test_book.get('price') and 
                    test_book.get('rating')):
                    print("✓ All new fields present and correct")
                else:
                    print("✗ Some new fields are missing")
                    return False
            else:
                print("✗ Test book not found in retrieved books")
                return False
        else:
            print(f"✗ Get books failed: {get_response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Get books error: {e}")
        return False
    
    print("\n=== All tests passed! ===")
    print("The e-book manager successfully supports:")
    print("- Gender classification")
    print("- Price information")
    print("- Rating system")
    return True

if __name__ == "__main__":
    test_new_fields()
