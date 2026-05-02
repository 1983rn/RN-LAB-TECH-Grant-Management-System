#!/usr/bin/env python3
"""
Database Migration: Add OTP and password change fields
"""
from database import get_db

def migrate_add_otp_fields():
    """Add must_change_password, otp_code, otp_expiry columns to schools table"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Check existing columns
        cursor.execute("PRAGMA table_info(schools)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'must_change_password' not in columns:
            print("Adding must_change_password column...")
            cursor.execute('ALTER TABLE schools ADD COLUMN must_change_password INTEGER DEFAULT 0')
            print("✅ must_change_password column added")
        
        if 'otp_code' not in columns:
            print("Adding otp_code column...")
            cursor.execute('ALTER TABLE schools ADD COLUMN otp_code TEXT')
            print("✅ otp_code column added")
        
        if 'otp_expiry' not in columns:
            print("Adding otp_expiry column...")
            cursor.execute('ALTER TABLE schools ADD COLUMN otp_expiry TEXT')
            print("✅ otp_expiry column added")
        
        print("✅ All OTP columns verified")

if __name__ == '__main__':
    migrate_add_otp_fields()
    print("Migration completed!")
