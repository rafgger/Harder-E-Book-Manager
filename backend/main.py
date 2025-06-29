# FastAPI backend for E-Book Manager
# Requirements: fastapi, uvicorn, asyncpg, sqlalchemy

from fastapi import FastAPI, HTTPException, Depends, Request
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

security = HTTPBasic()

# Simple in-memory session store
sessions = set()

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
async def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_password = config.PASSWORD
    if not secrets.compare_digest(credentials.password, correct_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    # Add session token logic if needed
    return True

@app.post("/login")
async def login(credentials: HTTPBasicCredentials = Depends(security)):
    correct_password = config.PASSWORD
    if not secrets.compare_digest(credentials.password, correct_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    # Generate a simple session token
    token = secrets.token_hex(16)
    sessions.add(token)
    return {"token": token}

@app.post("/books")
async def add_book(book: dict, auth: bool = Depends(authenticate)):
    # Validation
    required = ["ISBN", "title", "author", "year", "publisher", "cover"]
    for field in required:
        if field not in book or not book[field]:
            raise HTTPException(status_code=400, detail=f"Missing field: {field}")
    async with SessionLocal() as session:
        new_book = Book()
        new_book.isbn = book["ISBN"]
        new_book.title = book["title"]
        new_book.author = book["author"]
        new_book.year = book["year"]
        new_book.publisher = book["publisher"]
        new_book.cover = book["cover"]
        session.add(new_book)
        try:
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Book added"}

@app.post("/import-books")
async def import_books(auth: bool = Depends(authenticate)):
    # Import books from books.json
    try:
        with open("../books.json", "r", encoding="utf-8") as f:
            books = json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read books.json: {e}")
    imported = 0
    async with SessionLocal() as session:
        for book in books:
            if not all(k in book for k in ["ISBN", "title", "author", "year", "publisher", "cover"]):
                continue
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
