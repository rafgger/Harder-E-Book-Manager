import requests
import json
import sys

def test_backend():
    base_url = "http://localhost:8000"
    
    print("=" * 50)
    print("BACKEND END-TO-END TEST")
    print("=" * 50)
    
    try:
        # Test 1: Server connectivity
        print("\n1. Testing server connectivity...")
        response = requests.get(base_url, timeout=5)
        print(f"   Server status: {response.status_code}")
        
        # Test 2: Login
        print("\n2. Testing login...")
        login_data = {"username": "user", "password": "pass"}
        login_response = requests.post(f"{base_url}/login", json=login_data, timeout=5)
        print(f"   Login status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            token = token_data.get("token")
            print(f"   Token received: {token}")
            
            # Test 3: Add book with new token
            print("\n3. Testing add-book with fresh token...")
            book_data = {
                "ISBN": "end-to-end-test-123",
                "title": "End-to-End Test Book",
                "author": "Test Author",
                "year": 2025,
                "publisher": "Test Publisher",
                "cover": "http://example.com/test-cover.jpg"
            }
            
            headers = {"Authorization": f"Bearer {token}"}
            book_response = requests.post(f"{base_url}/add-book", json=book_data, headers=headers, timeout=5)
            print(f"   Add-book status: {book_response.status_code}")
            print(f"   Add-book response: {book_response.text}")
            
            # Test 4: Test with problematic frontend token
            print("\n4. Testing with frontend token...")
            frontend_token = "6f84f861a8384eebd0bb7ba5f1af50f9"
            frontend_headers = {"Authorization": f"Bearer {frontend_token}"}
            
            frontend_book_data = {
                "ISBN": "frontend-token-test",
                "title": "Frontend Token Test",
                "author": "Frontend Author",
                "year": 2025,
                "publisher": "Frontend Publisher",
                "cover": "http://example.com/frontend-cover.jpg"
            }
            
            frontend_response = requests.post(f"{base_url}/add-book", json=frontend_book_data, headers=frontend_headers, timeout=5)
            print(f"   Frontend token status: {frontend_response.status_code}")
            print(f"   Frontend token response: {frontend_response.text}")
            
            if frontend_response.status_code == 401:
                print("   *** FOUND THE ISSUE! Frontend token is invalid! ***")
            elif frontend_response.status_code == 200:
                print("   *** Frontend token works! Issue might be elsewhere! ***")
                
        else:
            print(f"   Login failed: {login_response.text}")
            
    except requests.exceptions.ConnectionError:
        print("   ERROR: Cannot connect to backend server")
        print("   Make sure the server is running on localhost:8000")
        return False
    except requests.exceptions.Timeout:
        print("   ERROR: Request timed out")
        return False
    except Exception as e:
        print(f"   ERROR: {str(e)}")
        return False
    
    print("\n" + "=" * 50)
    print("TEST COMPLETED")
    print("=" * 50)
    return True

if __name__ == "__main__":
    test_backend()
