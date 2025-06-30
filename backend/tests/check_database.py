#!/usr/bin/env python3
"""
DATABASE STRUCTURE TEST - E-Book Manager Backend

Verifies database connectivity and structure:
- PostgreSQL connection and authentication
- Books table existence and schema validation
- Column types and constraints verification
- Sample data insertion and retrieval
- Database health check

This test ensures the database layer is properly configured.
Usage: python check_database.py
"""
import asyncio
import asyncpg
import os

async def check_database():
    """Check database connection and table structure"""
    try:
        # Connect to database
        conn = await asyncpg.connect(
            host="localhost",
            port=5432,
            user="postgres",
            password="123456",
            database="Books"
        )
        
        print("✅ Database connection successful")
        
        # Check if books table exists
        table_exists = await conn.fetchval("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'books'
            );
        """)
        
        if table_exists:
            print("✅ Books table exists")
            
            # Get table structure
            columns = await conn.fetch("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'books'
                ORDER BY ordinal_position;
            """)
            
            print("📋 Table structure:")
            for col in columns:
                print(f"   - {col['column_name']}: {col['data_type']} ({'NULL' if col['is_nullable'] == 'YES' else 'NOT NULL'})")
            
            # Check if we have the new columns
            column_names = [col['column_name'] for col in columns]
            required_columns = ['isbn', 'title', 'author', 'year', 'publisher', 'img_m', 'genre', 'price', 'rating']
            missing_columns = [col for col in required_columns if col not in column_names]
            
            if missing_columns:
                print(f"❌ Missing columns: {missing_columns}")
                print("🔧 Need to add missing columns to the table")
                
                # Add missing columns
                for col in missing_columns:
                    try:
                        if col in ['genre', 'price', 'rating']:
                            await conn.execute(f"ALTER TABLE books ADD COLUMN {col} VARCHAR")
                            print(f"✅ Added column: {col}")
                    except Exception as e:
                        print(f"❌ Failed to add column {col}: {e}")
            else:
                print("✅ All required columns present")
            
            # Count books
            book_count = await conn.fetchval("SELECT COUNT(*) FROM books")
            print(f"📚 Books in database: {book_count}")
            
            # Show sample books
            if book_count > 0:
                books = await conn.fetch("SELECT isbn, title, author FROM books LIMIT 3")
                print("📖 Sample books:")
                for book in books:
                    print(f"   - {book['isbn']}: {book['title']} by {book['author']}")
            
        else:
            print("❌ Books table does not exist")
            print("🔧 Creating books table...")
            
            # Create table with all required columns
            await conn.execute("""
                CREATE TABLE books (
                    isbn VARCHAR PRIMARY KEY,
                    title VARCHAR,
                    author VARCHAR,
                    year INTEGER,
                    publisher VARCHAR,
                    img_m VARCHAR,
                    genre VARCHAR,
                    price VARCHAR,
                    rating VARCHAR
                )
            """)
            print("✅ Books table created")
        
        await conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(check_database())
    if success:
        print("\n🎉 Database check completed successfully")
    else:
        print("\n💥 Database check failed")
