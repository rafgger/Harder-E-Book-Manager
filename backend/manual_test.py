#!/usr/bin/env python3
"""
Manual test to reproduce the exact issue from the frontend logs
"""

# Test the exact token from the frontend logs
test_token = "353076b4753550a6bc6b8810e4ec3fb3"

print("=== Manual Test ===")
print(f"Testing token: {test_token}")

# Check if this token exists in sessions.pkl
import pickle
import os

SESSIONS_FILE = os.path.join(os.path.dirname(__file__), "sessions.pkl")

try:
    with open(SESSIONS_FILE, "rb") as f:
        sessions_data = pickle.load(f)
        sessions = set(sessions_data) if isinstance(sessions_data, list) else sessions_data
        print(f"Sessions from file: {sessions}")
        print(f"Is test token in sessions? {test_token in sessions}")
        
        if test_token not in sessions:
            print("❌ Token not found in sessions!")
            print("This explains why authentication is failing.")
        else:
            print("✅ Token found in sessions.")
            
except Exception as e:
    print(f"Error: {e}")

# Also test with a fresh login token
import secrets
print(f"\n=== Fresh Token Test ===")
fresh_token = secrets.token_hex(16)
print(f"Fresh token: {fresh_token}")

# Add it to sessions and save
try:
    with open(SESSIONS_FILE, "rb") as f:
        sessions_data = pickle.load(f)
        sessions = set(sessions_data) if isinstance(sessions_data, list) else sessions_data
    
    sessions.add(fresh_token)
    
    with open(SESSIONS_FILE, "wb") as f:
        pickle.dump(list(sessions), f)
    
    print(f"Added fresh token to sessions and saved.")
    
    # Verify it was saved
    with open(SESSIONS_FILE, "rb") as f:
        sessions_data = pickle.load(f)
        sessions = set(sessions_data) if isinstance(sessions_data, list) else sessions_data
        
    print(f"Verification - is fresh token in sessions? {fresh_token in sessions}")
    
except Exception as e:
    print(f"Error during fresh token test: {e}")
