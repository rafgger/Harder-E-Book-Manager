#!/usr/bin/env python3
"""
Test that matches exactly what the frontend sends
"""
import requests
import json

def test_frontend_exact():
    print("=== Frontend-Exact Test ===")
    
    base_url = "http://localhost:8000"
    
    try:
        # Step 1: Login exactly like frontend
        print("\n1. Login (frontend style)...")
        login_response = requests.post(
            f"{base_url}/login",
            auth=("", "123"),  # Empty username, password from config
            timeout=5
        )
        
        print(f"Login status: {login_response.status_code}")
        if login_response.status_code != 200:
            print(f"Login response: {login_response.text}")
            return False
            
        token_data = login_response.json()
        token = token_data["token"]
        print(f"Token received: {token}")
        
        # Step 2: Add book exactly like frontend would
        print("\n2. Add book (frontend style)...")
        
        # This is the exact payload the frontend sends
        book_payload = {
            "ISBN": "frontend-exact-test",
            "title": "Frontend Exact Test",
            "author": "Frontend Author",
            "year": 2025,
            "publisher": "Frontend Publisher", 
            "cover": "http://example.com/cover.jpg",
            "gender": "Fiction",  # Frontend sends "gender" to match backend expectation
            "price": "29.99",
            "rating": "4.2"
        }
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        print(f"Payload: {json.dumps(book_payload, indent=2)}")
        print(f"Headers: {headers}")
        
        add_response = requests.post(
            f"{base_url}/add-book",
            json=book_payload,
            headers=headers,
            timeout=5
        )
        
        print(f"Add-book status: {add_response.status_code}")
        print(f"Add-book response: {add_response.text}")
        
        if add_response.status_code == 200:
            print("✅ Frontend-exact test PASSED!")
            
            # Step 3: Verify book was added by getting all books
            print("\n3. Verify book was added...")
            books_response = requests.get(
                f"{base_url}/books",
                headers=headers,
                timeout=5
            )
            
            if books_response.status_code == 200:
                books = books_response.json()
                added_book = next((b for b in books if b["ISBN"] == "frontend-exact-test"), None)
                if added_book:
                    print("✅ Book verification PASSED!")
                    print(f"Added book: {json.dumps(added_book, indent=2)}")
                else:
                    print("❌ Book not found in database")
            
            return True
        else:
            print("❌ Frontend-exact test FAILED!")
            return False
            
    except Exception as e:
        print(f"❌ Test exception: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_frontend_exact()
    if success:
        print("\n🎉 All tests passed! Backend is working correctly.")
    else:
        print("\n💥 Tests failed. Check the error messages above.")
