import pickle
import os

SESSIONS_FILE = os.path.join(os.path.dirname(__file__), "sessions.pkl")

try:
    with open(SESSIONS_FILE, "rb") as f:
        sessions = pickle.load(f)
        print("Sessions loaded from file:", sessions)
        print("Number of sessions:", len(sessions))
        for i, token in enumerate(sessions):
            print(f"Token {i+1}: {token}")
except Exception as e:
    print("Error loading sessions:", e)
