#!/usr/bin/env python3
"""
Test the specific token that was causing 401 errors in the frontend
"""

import requests

BASE_URL = "http://localhost:8000"
PROBLEMATIC_TOKEN = "6f84f861a8384eebd0bb7ba5f1af50f9"

def test_problematic_token():
    """Test the specific token from the frontend logs"""
    print("=== Testing Problematic Token ===")
    print(f"Testing token: {PROBLEMATIC_TOKEN}")
    
    book_data = {
        "ISBN": "123",
        "title": "Default Title",
        "author": "Default Author",
        "year": 2025,
        "publisher": "Default Publisher",
        "cover": "http://example.com/default-cover.jpg"
    }
    
    headers = {"Authorization": f"Bearer {PROBLEMATIC_TOKEN}"}
    
    try:
        response = requests.post(f"{BASE_URL}/add-book", json=book_data, headers=headers)
        print(f"Response status: {response.status_code}")
        print(f"Response text: {response.text}")
        
        if response.status_code == 401:
            print("❌ TOKEN IS INVALID - This explains the frontend 401 error!")
            return False
        elif response.status_code == 200:
            print("✅ TOKEN IS VALID - The issue might be with CORS or request format")
            return True
        else:
            print(f"⚠️ Unexpected status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Error testing token: {e}")
        return False

def test_fresh_login_and_compare():
    """Login to get a fresh token and compare behavior"""
    print("\n=== Testing Fresh Login ===")
    
    try:
        # Login to get fresh token
        login_response = requests.post(f"{BASE_URL}/login", auth=("user", "123"))
        print(f"Login status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            fresh_token = login_response.json()["token"]
            print(f"Fresh token: {fresh_token}")
            
            # Test with fresh token
            book_data = {
                "ISBN": "fresh-test-123",
                "title": "Fresh Token Test",
                "author": "Fresh Author",
                "year": 2025,
                "publisher": "Fresh Publisher",
                "cover": "http://example.com/fresh-cover.jpg"
            }
            
            headers = {"Authorization": f"Bearer {fresh_token}"}
            response = requests.post(f"{BASE_URL}/add-book", json=book_data, headers=headers)
            
            print(f"Fresh token test status: {response.status_code}")
            print(f"Fresh token test response: {response.text}")
            
            if response.status_code == 200:
                print("✅ Fresh token works fine")
                return True
            else:
                print("❌ Fresh token also fails")
                return False
        else:
            print("❌ Login failed")
            return False
            
    except Exception as e:
        print(f"Error with fresh login test: {e}")
        return False

def main():
    print("Testing the specific token that caused frontend 401 errors...")
    
    # Test server connectivity
    try:
        response = requests.get(BASE_URL)
        print(f"Server is running: {response.status_code}")
    except Exception as e:
        print(f"Server not reachable: {e}")
        return
    
    # Test the problematic token
    problematic_result = test_problematic_token()
    
    # Test with fresh login
    fresh_result = test_fresh_login_and_compare()
    
    print(f"\n=== RESULTS ===")
    print(f"Problematic token ({PROBLEMATIC_TOKEN}): {'✅ Valid' if problematic_result else '❌ Invalid'}")
    print(f"Fresh login token: {'✅ Valid' if fresh_result else '❌ Invalid'}")
    
    if not problematic_result and fresh_result:
        print("\n🎯 DIAGNOSIS: The frontend token is expired/invalid!")
        print("   Solution: The frontend needs to login again to get a fresh token.")
    elif problematic_result and fresh_result:
        print("\n🤔 DIAGNOSIS: Both tokens work from Python, but frontend gets 401.")
        print("   This suggests a CORS, request format, or authentication header issue.")
    elif not fresh_result:
        print("\n⚠️ DIAGNOSIS: Even fresh tokens don't work - backend issue!")

if __name__ == "__main__":
    main()
