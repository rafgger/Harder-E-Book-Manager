#!/usr/bin/env python3
"""
Check which column (genre vs genre) has the actual data
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import asyncpg

async def check_columns():
    print("=== Checking Genre vs Genre Columns ===")
    
    try:
        conn = await asyncpg.connect(
            user="postgres",
            password="password",
            database="Books",
            host="localhost"
        )
        
        # Check both columns
        print("\n1. Checking sample data in both columns...")
        books = await conn.fetch("""
            SELECT isbn, title, genre, genre 
            FROM books 
            WHERE genre IS NOT NULL OR genre IS NOT NULL
            LIMIT 5
        """)
        
        print("Sample books with genre/genre data:")
        for book in books:
            print(f"   {book['isbn']}: genre='{book['genre']}', genre='{book['genre']}'")
        
        # Count non-null values in each column
        gender_count = await conn.fetchval("SELECT COUNT(*) FROM books WHERE genre IS NOT NULL AND genre != ''")
        genre_count = await conn.fetchval("SELECT COUNT(*) FROM books WHERE genre IS NOT NULL AND genre != ''")
        
        print(f"\n2. Data distribution:")
        print(f"   Books with 'genre' data: {gender_count}")
        print(f"   Books with 'genre' data: {genre_count}")
        
        # Check if we should use genre column instead
        if genre_count > gender_count:
            print(f"\n⚠️  The 'genre' column has more data ({genre_count}) than 'genre' ({gender_count})")
            print("   Consider updating the Book model to use the 'genre' column")
        else:
            print(f"\n✓ The 'genre' column is correctly being used")
        
        await conn.close()
        
    except Exception as e:
        print(f"❌ Error checking columns: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(check_columns())
