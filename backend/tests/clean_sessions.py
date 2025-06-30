#!/usr/bin/env python3
"""
Clean up sessions and test authentication directly
"""
import os
import pickle
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from main import load_sessions, save_sessions, SESSIONS_FILE
import secrets

def clean_and_test_sessions():
    print("=== Cleaning and Testing Sessions ===")
    
    # Step 1: Clean up corrupted sessions file
    print("\n1. Cleaning up sessions file...")
    if os.path.exists(SESSIONS_FILE):
        try:
            with open(SESSIONS_FILE, "rb") as f:
                old_data = pickle.load(f)
            print(f"Old sessions data: {old_data}")
            print(f"Old data type: {type(old_data)}")
        except Exception as e:
            print(f"Error reading old sessions: {e}")
        
        # Remove the corrupted file
        os.remove(SESSIONS_FILE)
        print("Removed old sessions file")
    
    # Step 2: Create a fresh sessions file with a test token
    print("\n2. Creating fresh sessions...")
    test_token = secrets.token_hex(16)
    sessions = {test_token}
    save_sessions(sessions)
    print(f"Created fresh sessions with test token: {test_token}")
    
    # Step 3: Test loading
    print("\n3. Testing session loading...")
    loaded_sessions = load_sessions()
    print(f"Loaded sessions: {loaded_sessions}")
    print(f"Loaded sessions type: {type(loaded_sessions)}")
    print(f"Is test token in loaded sessions? {test_token in loaded_sessions}")
    
    # Step 4: Test the exact token from frontend logs
    frontend_token = "353076b4753550a6bc6b8810e4ec3fb3"
    print(f"\n4. Testing frontend token: {frontend_token}")
    sessions.add(frontend_token)
    save_sessions(sessions)
    
    # Reload and test
    loaded_sessions = load_sessions()
    print(f"Sessions after adding frontend token: {loaded_sessions}")
    print(f"Is frontend token in sessions? {frontend_token in loaded_sessions}")
    
    return test_token, frontend_token

if __name__ == "__main__":
    clean_and_test_sessions()
