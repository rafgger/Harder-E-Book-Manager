#!/usr/bin/env python3
"""
Test the authentication logic directly without running the server
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from main import load_sessions

def test_auth_logic():
    print("=== Testing Authentication Logic ===")
    
    # Test the exact scenario from the frontend
    frontend_token = "d5254ec17e49466a839e8ee110ecf453"  # Updated token
    authorization_header = f"Bearer {frontend_token}"
    
    print(f"Authorization header: {authorization_header}")
    
    # Simulate what the authenticate function does
    sessions = load_sessions()
    print(f"Loaded sessions: {sessions}")
    print(f"Sessions type: {type(sessions)}")
    
    if authorization_header and authorization_header.startswith("Bearer "):
        token = authorization_header.split(" ", 1)[1]
        print(f"Extracted token: {token}")
        print(f"Token type: {type(token)}")
        print(f"Is token in sessions? {token in sessions}")
        
        if token in sessions:
            print("✅ Authentication would SUCCEED")
            return True
        else:
            print("❌ Authentication would FAIL")
            print("All tokens in sessions:")
            for i, session_token in enumerate(sessions):
                print(f"  {i}: {session_token} (type: {type(session_token)})")
                print(f"     token == session_token: {token == session_token}")
            return False
    else:
        print("❌ Authorization header format is invalid")
        return False

if __name__ == "__main__":
    test_auth_logic()
