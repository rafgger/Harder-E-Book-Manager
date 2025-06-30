#!/usr/bin/env python3
"""
Direct backend diagnostic to identify the 500 error cause
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import json
from main import SessionLocal, Book, authenticate
from sqlalchemy.future import select

async def test_book_creation_directly():
    print("=== Direct Backend Book Creation Test ===")
    
    try:
        # Test 1: Database connection
        print("\n1. Testing database connection...")
        async with SessionLocal() as session:
            result = await session.execute(select(Book).limit(1))
            books = result.scalars().all()
            print(f"✅ Database connection successful. Found {len(books)} existing books")
        
        # Test 2: Test Book model creation in memory
        print("\n2. Testing Book model creation...")
        test_book = Book(
            isbn="diagnostic-500-test",
            title="500 Error Diagnostic",
            author="Test Author",
            year=2025,
            publisher="Test Publisher",
            cover="http://example.com/cover.jpg",
            gender="Fiction",
            price=19.99,  # Numeric value
            rating=4.5    # Numeric value
        )
        print("✅ Book model creation successful")
        print(f"   Book attributes: isbn={test_book.isbn}, gender={test_book.gender}, price={test_book.price}, rating={test_book.rating}")
        
        # Test 3: Test database insertion
        print("\n3. Testing database insertion...")
        async with SessionLocal() as session:
            # Check if book already exists
            existing = await session.execute(select(Book).where(Book.isbn == "diagnostic-500-test"))
            if existing.scalar_one_or_none():
                print("✅ Test book already exists, skipping insertion")
            else:
                session.add(test_book)
                await session.commit()
                print("✅ Database insertion successful")
        
        # Test 4: Test the exact data from the frontend test
        print("\n4. Testing with exact frontend test data...")
        frontend_book_data = {
            "ISBN": "test-book-frontend-500",
            "title": "Test Book Title", 
            "author": "Test Author",
            "year": 2025,
            "publisher": "Test Publisher",
            "cover": "http://example.com/test-cover.jpg",
            "gender": "Fiction",
            "price": "19.99",  # String as received from frontend
            "rating": "4.5"    # String as received from frontend
        }
        
        # Convert price and rating like the endpoint does
        try:
            price_value = float(frontend_book_data["price"]) if frontend_book_data["price"] else None
            rating_value = float(frontend_book_data["rating"]) if frontend_book_data["rating"] else None
            print(f"✅ Price/rating conversion successful: price={price_value}, rating={rating_value}")
        except ValueError as e:
            print(f"❌ Price/rating conversion failed: {e}")
            return False
        
        # Create book with converted values
        frontend_book = Book(
            isbn=frontend_book_data["ISBN"],
            title=frontend_book_data["title"],
            author=frontend_book_data["author"],
            year=frontend_book_data["year"],
            publisher=frontend_book_data["publisher"],
            cover=frontend_book_data["cover"],
            gender=frontend_book_data["gender"],
            price=price_value,
            rating=rating_value
        )
        
        async with SessionLocal() as session:
            # Check if book already exists
            existing = await session.execute(select(Book).where(Book.isbn == frontend_book_data["ISBN"]))
            if existing.scalar_one_or_none():
                print("✅ Frontend test book already exists, skipping insertion")
            else:
                session.add(frontend_book)
                await session.commit()
                print("✅ Frontend test book insertion successful")
        
        print("\n🎉 All direct backend tests passed!")
        print("The 500 error might be related to session handling or async context issues")
        return True
        
    except Exception as e:
        print(f"\n❌ Direct backend test failed!")
        print(f"   Error: {e}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        print("\n--- Full Error Traceback ---")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_book_creation_directly())
    if not success:
        print("\n💥 Direct backend test failed - this explains the 500 error!")
        sys.exit(1)
    else:
        print("\n✅ Direct backend test passed - the 500 error might be in the HTTP endpoint handling")
