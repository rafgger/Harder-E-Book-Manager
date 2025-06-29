#!/usr/bin/env python3
"""
Read and display the contents of sessions.pkl
"""
import pickle
import os

SESSIONS_FILE = os.path.join(os.path.dirname(__file__), "sessions.pkl")

def read_sessions_file():
    print("=== Reading sessions.pkl ===")
    print(f"File path: {SESSIONS_FILE}")
    print(f"File exists: {os.path.exists(SESSIONS_FILE)}")
    
    if not os.path.exists(SESSIONS_FILE):
        print("No sessions file found!")
        return
    
    try:
        with open(SESSIONS_FILE, "rb") as f:
            sessions = pickle.load(f)
            print(f"Raw data from file: {sessions}")
            print(f"Data type: {type(sessions)}")
            
            if isinstance(sessions, list):
                print(f"Number of sessions: {len(sessions)}")
                for i, token in enumerate(sessions):
                    print(f"Token {i}: {token} (type: {type(token)})")
            elif isinstance(sessions, set):
                print(f"Number of sessions: {len(sessions)}")
                for i, token in enumerate(sessions):
                    print(f"Token {i}: {token} (type: {type(token)})")
            else:
                print(f"Unexpected data type: {type(sessions)}")
                
    except Exception as e:
        print(f"Error reading sessions file: {e}")

if __name__ == "__main__":
    read_sessions_file()
