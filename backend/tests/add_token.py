#!/usr/bin/env python3
"""
Add the current frontend token to sessions
"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from main import load_sessions, save_sessions

def add_frontend_token():
    print("=== Adding Frontend Token ===")
    
    # The token from the latest frontend logs
    frontend_token = "d5254ec17e49466a839e8ee110ecf453"
    
    # Load current sessions
    sessions = load_sessions()
    print(f"Current sessions: {sessions}")
    
    # Add the frontend token
    sessions.add(frontend_token)
    print(f"Added token: {frontend_token}")
    
    # Save back to file
    save_sessions(sessions)
    print("Saved sessions to file")
    
    # Verify it was saved
    updated_sessions = load_sessions()
    print(f"Updated sessions: {updated_sessions}")
    print(f"Is frontend token in sessions? {frontend_token in updated_sessions}")

if __name__ == "__main__":
    add_frontend_token()
