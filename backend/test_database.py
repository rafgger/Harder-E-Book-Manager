#!/usr/bin/env python3
"""
Database connectivity test
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.future import select
import os
import sys

# Add the backend directory to the path so we can import main
sys.path.append(os.path.dirname(__file__))
from main import Book, DATABASE_URL, Base

async def test_database():
    print("=== Database Connectivity Test ===")
    
    try:
        # Test 1: Create engine
        print("\n1. Testing database engine creation...")
        engine = create_async_engine(DATABASE_URL, echo=True)
        print("✅ Engine created successfully")
        
        # Test 2: Create session
        print("\n2. Testing session creation...")
        SessionLocal = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        print("✅ Session factory created successfully")
        
        # Test 3: Test database connection
        print("\n3. Testing database connection...")
        async with SessionLocal() as session:
            # Try to execute a simple query
            result = await session.execute(select(Book).limit(1))
            books = result.scalars().all()
            print(f"✅ Database connection successful. Found {len(books)} books")
            
        # Test 4: Test book creation
        print("\n4. Testing book creation...")
        test_book = Book(
            isbn="db-test-123",
            title="Database Test Book",
            author="Test Author",
            year=2025,
            publisher="Test Publisher",
            cover="http://example.com/cover.jpg",
            genre="Fiction",
            price="19.99",
            rating="4.5"
        )
        
        async with SessionLocal() as session:
            # Check if book already exists
            existing = await session.execute(select(Book).where(Book.isbn == "db-test-123"))
            if existing.scalar_one_or_none():
                print("✅ Test book already exists in database")
            else:
                session.add(test_book)
                await session.commit()
                print("✅ Test book added successfully")
        
        print("\n🎉 All database tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Database test failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(test_database())
