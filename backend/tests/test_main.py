# import pytest
# from httpx import AsyncClient
import sys
import os

# Add the backend directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from main import app

import asyncio

from fastapi.testclient import TestClient

client = TestClient(app)

def test_get_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# def test_get_book_not_found():
#     response = client.get("/books/DOESNOTEXIST")
#     assert response.status_code == 404
#     assert response.json()["detail"] == "Book not found"
