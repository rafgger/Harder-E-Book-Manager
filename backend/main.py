# FastAPI backend for E-Book Manager
# Requirements: fastapi, uvicorn, asyncpg, sqlalchemy

from fastapi import FastAPI, HTTPException, Depends, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy.future import select
import os
import json
import config

from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
import pickle

security = HTTPBasic()

# Simple in-memory session store
SESSIONS_FILE = os.path.join(os.path.dirname(__file__), "sessions.pkl")

def load_sessions():
    try:
        with open(SESSIONS_FILE, "rb") as f:
            sessions_data = pickle.load(f)
            # Ensure we always return a set, regardless of what was stored
            if isinstance(sessions_data, list):
                sessions = set(sessions_data)
            elif isinstance(sessions_data, set):
                sessions = sessions_data
            else:
                sessions = set()
            print("[DEBUG] Loaded sessions from file:", sessions)  # Debug log
            return sessions
    except Exception as e:
        print("[DEBUG] Failed to load sessions:", str(e))  # Debug log
        return set()

def save_sessions(sessions):
    try:
        with open(SESSIONS_FILE, "wb") as f:
            pickle.dump(list(sessions), f)
            print("[DEBUG] Saved sessions to file:", sessions)  # Debug log
    except Exception as e:
        print("[DEBUG] Failed to save sessions:", str(e))  # Debug log

sessions = load_sessions()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:123456@localhost:5432/Books"
)

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
Base = declarative_base()

class Book(Base):
    __tablename__ = "books"
    isbn = Column("isbn", String, primary_key=True, index=True)
    title = Column("title", String)
    author = Column("author", String)
    year = Column("year", Integer)
    publisher = Column("publisher", String)
    cover = Column("img_m", String)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/books")
async def get_books():
    async with SessionLocal() as session:
        result = await session.execute(select(Book))
        books = result.scalars().all()
        return [
            {
                "ISBN": b.isbn,
                "title": b.title,
                "author": b.author,
                "year": b.year,
                "publisher": b.publisher,
                "cover": b.cover
            }
            for b in books
        ]

@app.get("/books/{isbn}")
async def get_book(isbn: str):
    async with SessionLocal() as session:
        result = await session.execute(select(Book).where(Book.isbn == isbn))
        book = result.scalar_one_or_none()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return {
            "ISBN": book.isbn,
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "publisher": book.publisher,
            "cover": book.cover
        }

# Authentication dependency
async def authenticate(
    credentials: HTTPBasicCredentials = Depends(security),
    authorization: str = Header(None)
):
    # Always reload sessions from disk to get the latest tokens
    global sessions
    sessions = load_sessions()
    print("[DEBUG] Incoming Authorization header:", authorization)
    print("[DEBUG] Current session tokens:", sessions)
    print("[DEBUG] Sessions file path:", SESSIONS_FILE)
    print("[DEBUG] Sessions file exists:", os.path.exists(SESSIONS_FILE))
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ", 1)[1]
        print("[DEBUG] Extracted token:", token)
        print("[DEBUG] Token type:", type(token))
        print("[DEBUG] Sessions type:", type(sessions))
        print("[DEBUG] Is token in sessions?:", token in sessions)
        if token in sessions:
            print("[DEBUG] Token is valid.")
            return True
        print("[DEBUG] Token is invalid or expired.")
        print("[DEBUG] All tokens in sessions:")
        for i, session_token in enumerate(sessions):
            print(f"[DEBUG]   {i}: {session_token} (type: {type(session_token)})")
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    correct_password = config.PASSWORD
    if not secrets.compare_digest(credentials.password, correct_password):
        print("[DEBUG] Incorrect password for HTTP Basic Auth.")
        raise HTTPException(status_code=401, detail="Incorrect password")
    print("[DEBUG] HTTP Basic Auth successful.")
    return True

@app.post("/login")
async def login(credentials: HTTPBasicCredentials = Depends(security)):
    global sessions
    correct_password = config.PASSWORD
    if not secrets.compare_digest(credentials.password, correct_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    # Generate a simple session token and reload sessions to ensure consistency
    token = secrets.token_hex(16)
    sessions = load_sessions()
    sessions.add(token)
    save_sessions(sessions)
    print("[DEBUG] Generated new token and saved to sessions:", token)
    return {"token": token}

@app.post("/add-book")
async def add_book(book: dict, auth: bool = Depends(authenticate)):
    try:
        # Validation
        required = ["ISBN", "title", "author", "year", "publisher", "cover"]
        for field in required:
            if field not in book:
                raise HTTPException(status_code=400, detail=f"Missing field: {field}")

        # Simulate adding the book (replace with actual logic)
        print("[DEBUG] Adding book:", book)
        return {"message": "Book added successfully"}
    except Exception as e:
        print("[ERROR] Exception in /add-book:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/import-books")
async def import_books(auth: bool = Depends(authenticate)):
    # Import books from books.json
    try:
        with open("../books.json", "r", encoding="utf-8") as f:
            books = json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read books.json: {e}")
    imported = 0
    async with AsyncSession(engine) as session:
        for book in books:
            if not all(k in book for k in ["ISBN", "title", "author", "year", "publisher", "cover"]):
                continue
            # Check if the book already exists
            result = await session.execute(select(Book).where(Book.isbn == book["ISBN"]))
            existing = result.scalar_one_or_none()
            if existing:
                continue  # Skip duplicates
            new_book = Book()
            new_book.isbn = book["ISBN"]
            new_book.title = book["title"]
            new_book.author = book["author"]
            new_book.year = book["year"]
            new_book.publisher = book["publisher"]
            new_book.cover = book["cover"]
            session.add(new_book)
            imported += 1
        try:
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail=str(e))
    return {"imported": imported}
