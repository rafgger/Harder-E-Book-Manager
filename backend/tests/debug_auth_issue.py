#!/usr/bin/env python3
"""
Debug the exact issue with session persistence
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import the session functions from main.py
from main import load_sessions, save_sessions, SESSIONS_FILE
import secrets

def debug_session_issue():
    print("=== Debugging Session Issue ===")
    print(f"Sessions file path: {SESSIONS_FILE}")
    print(f"Sessions file exists: {os.path.exists(SESSIONS_FILE)}")
    
    # Simulate what happens during login
    print("\n--- Simulating Login ---")
    sessions = load_sessions()
    print(f"Loaded sessions: {sessions}")
    
    # Generate a token like the login endpoint does
    token = secrets.token_hex(16)
    sessions.add(token)
    save_sessions(sessions)
    print(f"Generated token: {token}")
    print(f"Sessions after adding token: {sessions}")
    
    # Simulate what happens during authentication
    print("\n--- Simulating Authentication ---")
    auth_sessions = load_sessions()
    print(f"Auth loaded sessions: {auth_sessions}")
    print(f"Is token in auth sessions? {token in auth_sessions}")
    
    # Check types and values
    print(f"Token type: {type(token)}")
    print(f"Auth sessions type: {type(auth_sessions)}")
    
    if auth_sessions:
        for i, session_token in enumerate(auth_sessions):
            print(f"Session {i}: {session_token} (type: {type(session_token)})")
            print(f"Token == session_token: {token == session_token}")

if __name__ == "__main__":
    debug_session_issue()
