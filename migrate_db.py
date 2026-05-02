#!/usr/bin/env python3
"""
Database Migration Script
Adds missing columns to existing database
"""
from database import get_db

def migrate_database():
    """Add missing columns to schools table"""
    print("🔄 Running database migration...")
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Add subscription_type column
        try:
            cursor.execute('ALTER TABLE schools ADD COLUMN subscription_type TEXT DEFAULT "TRIAL"')
            print("✅ Added subscription_type column")
        except Exception as e:
            print(f"ℹ️  subscription_type column already exists or error: {e}")
        
        # Add expiry_date column
        try:
            cursor.execute('ALTER TABLE schools ADD COLUMN expiry_date DATE')
            print("✅ Added expiry_date column")
        except Exception as e:
            print(f"ℹ️  expiry_date column already exists or error: {e}")
        
        # Set default values for existing schools
        try:
            cursor.execute('''
                UPDATE schools 
                SET subscription_type = 'TRIAL', 
                    expiry_date = subscription_end
                WHERE subscription_type IS NULL
            ''')
            print("✅ Updated existing schools with default values")
        except Exception as e:
            print(f"⚠️  Error updating defaults: {e}")
    
    print("✅ Migration complete!")

if __name__ == '__main__':
    migrate_database()
