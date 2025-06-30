#!/usr/bin/env python3
"""
Check which column has the actual data using SQLAlchemy
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from main import SessionLocal, Book
from sqlalchemy.future import select

async def check_columns():
    print("=== Checking Gender vs Genre Columns ===")
    
    try:
        async with SessionLocal() as session:
            # Get a few books to see the current data structure
            result = await session.execute(select(Book).limit(5))
            books = result.scalars().all()
            
            print("Sample books from current Book model:")
            for book in books:
                print(f"   {book.isbn}: gender='{book.gender}', title='{book.title}'")
            
            # Count books with gender data
            result = await session.execute(select(Book).where(Book.gender.is_not(None)))
            books_with_gender = result.scalars().all()
            gender_count = len(books_with_gender)
            
            print(f"\nBooks with 'gender' data: {gender_count}")
            
            if gender_count > 0:
                print("✓ The Book model is correctly using the 'gender' column")
            else:
                print("⚠️  No books have 'gender' data - this might be the issue")
        
    except Exception as e:
        print(f"❌ Error checking columns: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(check_columns())
