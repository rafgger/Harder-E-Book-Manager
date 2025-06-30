#!/usr/bin/env python3
"""
Test books API endpoint
"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("🧪 Testing Books API Endpoint")

# Step 1: Test server connectivity
try:
    response = requests.get(f"{BASE_URL}/", timeout=5)
    print(f"✅ Server is running (status: {response.status_code})")
except Exception as e:
    print(f"❌ Server connection failed: {e}")
    exit(1)

# Step 2: Test login to get token
print("\n🔐 Testing login...")
try:
    response = requests.post(f"{BASE_URL}/login", auth=("user", "123"), timeout=5)
    if response.status_code == 200:
        token = response.json()["token"]
        print(f"✅ Login successful, token: {token[:20]}...")
    else:
        print(f"❌ Login failed: {response.status_code} - {response.text}")
        exit(1)
except Exception as e:
    print(f"❌ Login error: {e}")
    exit(1)

# Step 3: Test books endpoint with authentication
print("\n📚 Testing books endpoint...")
try:
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/books", headers=headers, timeout=5)
    
    if response.status_code == 200:
        books = response.json()
        print(f"✅ Books retrieved successfully: {len(books)} books found")
        
        if books:
            print("📖 Sample book:")
            book = books[0]
            for key, value in book.items():
                print(f"   {key}: {value}")
        else:
            print("📭 No books in database")
    else:
        print(f"❌ Books retrieval failed: {response.status_code} - {response.text}")
        
except Exception as e:
    print(f"❌ Books endpoint error: {e}")

print("\n🏁 Test completed")
