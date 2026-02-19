#!/usr/bin/env python3
"""
Database Migration: Add school_name column to school_settings table
"""
from database import get_db

def migrate_add_school_name_column():
    """Add school_name column to school_settings if it doesn't exist"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Check if column exists
        cursor.execute("PRAGMA table_info(school_settings)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'school_name' not in columns:
            print("Adding school_name column to school_settings table...")
            cursor.execute('''
                ALTER TABLE school_settings
                ADD COLUMN school_name TEXT
            ''')
            print("✅ Column added successfully")
        else:
            print("✅ Column school_name already exists")

if __name__ == '__main__':
    migrate_add_school_name_column()
    print("Migration completed!")
