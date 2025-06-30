#!/usr/bin/env python3
"""
Minimal server test
"""
import requests
import time

def minimal_test():
    print("=== Minimal Server Test ===")
    
    try:
        print("1. Testing server response...")
        start_time = time.time()
        response = requests.get("http://localhost:8000/docs", timeout=3)
        end_time = time.time()
        
        print(f"✅ Server responds in {end_time - start_time:.2f}s")
        print(f"Status: {response.status_code}")
        
        print("\n2. Testing login endpoint...")
        start_time = time.time()
        login_response = requests.post(
            "http://localhost:8000/login", 
            auth=("", "123"), 
            timeout=3
        )
        end_time = time.time()
        
        print(f"Login response in {end_time - start_time:.2f}s")
        print(f"Login status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            print(f"✅ Token received: {token_data['token'][:10]}...")
            return True
        else:
            print(f"❌ Login failed: {login_response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out - server may be slow or unresponsive")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = minimal_test()
    if success:
        print("\n🎉 Minimal test passed!")
    else:
        print("\n💥 Minimal test failed!")
