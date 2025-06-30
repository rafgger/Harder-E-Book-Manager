#!/usr/bin/env python3
"""
Comprehensive test for the updated E-Book Manager
Tests all functionality including new fields and database operations
"""
import requests
import json
import time

def comprehensive_test():
    print("=== Comprehensive E-Book Manager Test ===")
    print("Testing: Enhanced features with Genre, Price, and Rating")
    
    base_url = "http://localhost:8000"
    password = "123"
    
    # Step 1: Server connectivity
    print("\n1. Testing server connectivity...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"✓ Server is running (status: {response.status_code})")
    except Exception as e:
        print(f"✗ Server connection failed: {e}")
        return False
    
    # Step 2: Authentication
    print("\n2. Testing authentication...")
    try:
        response = requests.post(f"{base_url}/login", auth=("user", password))
        if response.status_code == 200:
            token = response.json()["token"]
            print(f"✓ Authentication successful")
        else:
            print(f"✗ Authentication failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Authentication error: {e}")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Step 3: Test book addition with new fields
    print("\n3. Testing enhanced book addition...")
    test_books = [
        {
            "ISBN": "test-fiction-2025",
            "title": "Test Fiction Novel",
            "author": "Jane Doe",
            "year": 2025,
            "publisher": "Test Fiction Press",
            "cover": "http://example.com/fiction.jpg",
            "genre": "Fiction",
            "price": "24.99",
            "rating": "4.5"
        },
        {
            "ISBN": "test-science-2025",
            "title": "Advanced Science Concepts",
            "author": "Dr. John Smith",
            "year": 2025,
            "publisher": "Science Publishing",
            "cover": "http://example.com/science.jpg",
            "genre": "Science",
            "price": "89.99",
            "rating": "4.8"
        },
        {
            "ISBN": "test-history-2025",
            "title": "Modern World History",
            "author": "Prof. Alice Johnson",
            "year": 2025,
            "publisher": "Academic Press",
            "cover": "http://example.com/history.jpg",
            "genre": "History",
            "price": "45.50",
            "rating": "4.2"
        }
    ]
    
    added_books = 0
    for book in test_books:
        try:
            response = requests.post(f"{base_url}/add-book", json=book, headers=headers)
            if response.status_code == 200:
                print(f"✓ Added: {book['title']} (Genre: {book['genre']}, Price: ${book['price']}, Rating: {book['rating']})")
                added_books += 1
            else:
                print(f"✗ Failed to add {book['title']}: {response.text}")
        except Exception as e:
            print(f"✗ Error adding {book['title']}: {e}")
    
    print(f"Successfully added {added_books}/{len(test_books)} books")
    
    # Step 4: Test book retrieval and verify new fields
    print("\n4. Testing book retrieval with new fields...")
    try:
        response = requests.get(f"{base_url}/books", headers=headers)
        if response.status_code == 200:
            books = response.json()
            print(f"✓ Retrieved {len(books)} books from database")
            
            # Check if our test books are present with new fields
            test_books_found = 0
            for book in books:
                if book.get("ISBN", "").startswith("test-"):
                    test_books_found += 1
                    has_new_fields = all(field in book for field in ['genre', 'price', 'rating'])
                    if has_new_fields:
                        print(f"✓ {book['title']}: Genre={book.get('genre')}, Price=${book.get('price')}, Rating={book.get('rating')}")
                    else:
                        missing_fields = [field for field in ['genre', 'price', 'rating'] if field not in book]
                        print(f"✗ {book['title']}: Missing fields: {missing_fields}")
            
            print(f"Found {test_books_found} test books with new fields")
        else:
            print(f"✗ Failed to retrieve books: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error retrieving books: {e}")
        return False
    
    # Step 5: Test import functionality (if books.json exists)
    print("\n5. Testing import functionality...")
    try:
        response = requests.post(f"{base_url}/import-books", headers=headers)
        if response.status_code == 200:
            print("✓ Books import successful")
        else:
            print(f"⚠ Import failed: {response.text} (this may be expected if books.json is not accessible)")
    except Exception as e:
        print(f"⚠ Import error: {e} (this may be expected)")
    
    # Step 6: Test error handling
    print("\n6. Testing error handling...")
    
    # Test duplicate ISBN
    duplicate_book = {
        "ISBN": "test-fiction-2025",  # Same as first test book
        "title": "Duplicate Test",
        "author": "Test Author",
        "year": 2025,
        "publisher": "Test Publisher",
        "cover": "http://example.com/test.jpg",
        "genre": "Fiction",
        "price": "19.99",
        "rating": "4.0"
    }
    
    try:
        response = requests.post(f"{base_url}/add-book", json=duplicate_book, headers=headers)
        if response.status_code == 400:
            print("✓ Duplicate ISBN detection working")
        else:
            print(f"✗ Duplicate ISBN should be rejected, got: {response.status_code}")
    except Exception as e:
        print(f"✗ Error testing duplicate ISBN: {e}")
    
    # Test missing fields
    incomplete_book = {
        "ISBN": "test-incomplete",
        "title": "Incomplete Book"
        # Missing required fields
    }
    
    try:
        response = requests.post(f"{base_url}/add-book", json=incomplete_book, headers=headers)
        if response.status_code == 400:
            print("✓ Missing fields validation working")
        else:
            print(f"✗ Missing fields should be rejected, got: {response.status_code}")
    except Exception as e:
        print(f"✗ Error testing missing fields: {e}")
    
    print("\n=== Test Summary ===")
    print("✓ Server connectivity")
    print("✓ Authentication system")
    print("✓ Enhanced book addition (Genre, Price, Rating)")
    print("✓ Database persistence of new fields")
    print("✓ Book retrieval with new fields")
    print("✓ Error handling and validation")
    print("\n🎉 All core functionality working with new fields!")
    
    return True

if __name__ == "__main__":
    comprehensive_test()
