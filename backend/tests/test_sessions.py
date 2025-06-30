#!/usr/bin/env python3
"""
Simple test script to verify the session persistence functionality
"""
import os
import sys
import pickle

# Add the current directory to Python path so we can import the functions
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from main import load_sessions, save_sessions, SESSIONS_FILE

def test_session_persistence():
    print("=== Testing Session Persistence ===")
    
    # Test 1: Start with a clean slate
    if os.path.exists(SESSIONS_FILE):
        os.remove(SESSIONS_FILE)
        print("Removed existing sessions.pkl")
    
    # Test 2: Load sessions (should be empty)
    sessions = load_sessions()
    print(f"Initial sessions: {sessions}")
    assert len(sessions) == 0, "Initial sessions should be empty"
    
    # Test 3: Add a token and save
    test_token = "test123456789abcdef"
    sessions.add(test_token)
    save_sessions(sessions)
    print(f"Added token and saved: {test_token}")
    
    # Test 4: Load sessions again (should contain the token)
    sessions2 = load_sessions()
    print(f"Reloaded sessions: {sessions2}")
    assert test_token in sessions2, f"Token {test_token} should be in reloaded sessions"
    
    # Test 5: Add another token
    test_token2 = "another123456789xyz"
    sessions2.add(test_token2)
    save_sessions(sessions2)
    print(f"Added second token and saved: {test_token2}")
    
    # Test 6: Final verification
    sessions3 = load_sessions()
    print(f"Final sessions: {sessions3}")
    assert test_token in sessions3, f"First token {test_token} should still be there"
    assert test_token2 in sessions3, f"Second token {test_token2} should be there"
    
    print("✅ All session persistence tests passed!")

if __name__ == "__main__":
    test_session_persistence()
