#!/usr/bin/env python3
"""
Diagnose the 500 Internal Server Error
"""
import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import SessionLocal, Book, engine
from sqlalchemy.future import select

async def diagnose_database():
    print("=== Database Diagnostic Test ===")
    
    try:
        print("\n1. Testing session creation...")
        async with SessionLocal() as session:
            print("✅ Session created successfully")
            
            print("\n2. Testing simple query...")
            result = await session.execute(select(Book).limit(1))
            books = result.scalars().all()
            print(f"✅ Simple query successful. Found {len(books)} existing books")
            
            print("\n3. Testing book creation (the failing operation)...")
            test_book = Book(
                isbn="diagnostic-test-book",
                title="Diagnostic Test",
                author="Test Author",
                year=2025,
                publisher="Test Publisher",
                cover="http://example.com/cover.jpg",
                gender="Fiction",  # This maps to 'gender' column in DB
                price="19.99",
                rating="4.5"
            )
            
            # Check if book already exists first
            existing = await session.execute(select(Book).where(Book.isbn == "diagnostic-test-book"))
            existing_book = existing.scalar_one_or_none()
            
            if existing_book:
                print("✅ Test book already exists, skipping creation")
            else:
                print("   Adding test book to session...")
                session.add(test_book)
                
                print("   Committing to database...")
                await session.commit()
                print("✅ Book creation and commit successful!")
            
            print("\n4. Testing book retrieval...")
            result = await session.execute(select(Book).where(Book.isbn == "diagnostic-test-book"))
            retrieved_book = result.scalar_one_or_none()
            
            if retrieved_book:
                print("✅ Book retrieval successful!")
                print(f"   ISBN: {retrieved_book.isbn}")
                print(f"   Title: {retrieved_book.title}")
                print(f"   Genre: {retrieved_book.gender}")
                print(f"   Price: {retrieved_book.price}")
                print(f"   Rating: {retrieved_book.rating}")
            else:
                print("❌ Book retrieval failed!")
                
    except Exception as e:
        print(f"\n❌ Database diagnostic failed!")
        print(f"   Error: {e}")
        print(f"   Error type: {type(e).__name__}")
        
        # Print full traceback for debugging
        import traceback
        print("\n--- Full Error Traceback ---")
        traceback.print_exc()
        return False
    
    print("\n🎉 All database operations successful!")
    return True

if __name__ == "__main__":
    success = asyncio.run(diagnose_database())
    if not success:
        print("\n💥 Database diagnostic failed - this explains the 500 error!")
        sys.exit(1)
    else:
        print("\n✅ Database is working - the 500 error might be elsewhere!")
