#!/usr/bin/env python3
"""
Fix Developer Login - Ensure Correct Credentials
"""
from database import get_db, hash_password, init_database, DATABASE_PATH
import os

print("=" * 60)
print("FIXING DEVELOPER LOGIN")
print("=" * 60)

# Ensure database exists
if not os.path.exists('data'):
    os.makedirs('data')
    print("✅ Created data directory")

if not os.path.exists(DATABASE_PATH):
    print("📦 Initializing database...")
    init_database()

# Fix developer account
print("\n🔧 Fixing developer account...")
with get_db() as conn:
    cursor = conn.cursor()
    
    # Delete existing developer account if any
    cursor.execute('DELETE FROM schools WHERE username = ?', ('juniornsambe@yahoo.com',))
    print("   Removed old developer account (if existed)")
    
    # Create fresh developer account with correct credentials
    username = 'juniornsambe@yahoo.com'
    password = 'blessings19831983/'
    password_hash = hash_password(password)
    
    cursor.execute('''
        INSERT INTO schools (school_name, username, password_hash, is_active, is_locked, subscription_status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('DEVELOPER_ACCOUNT', username, password_hash, 1, 0, 'LIFETIME'))
    
    print("✅ Created fresh developer account")
    
    # Verify it was created correctly
    cursor.execute('SELECT * FROM schools WHERE username = ?', (username,))
    dev = cursor.fetchone()
    
    if dev:
        print("\n✅ VERIFICATION:")
        print(f"   Username: {dev['username']}")
        print(f"   School Name: {dev['school_name']}")
        print(f"   Is Active: {dev['is_active']}")
        print(f"   Is Locked: {dev['is_locked']}")
        print(f"   Subscription: {dev['subscription_status']}")
        print(f"   Password Hash: {dev['password_hash'][:30]}...")
        
        # Test password verification
        from database import verify_password
        if verify_password(password, dev['password_hash']):
            print("\n✅ Password verification: SUCCESS")
        else:
            print("\n❌ Password verification: FAILED")
    
    conn.commit()

print("\n" + "=" * 60)
print("✅ DEVELOPER LOGIN FIXED!")
print("=" * 60)
print("\n🔐 Developer Credentials:")
print("   Username: juniornsambe@yahoo.com")
print("   Password: blessings19831983/")
print("\n💡 To login:")
print("   1. Open http://localhost:5176")
print("   2. Type 'devaccess' on login screen")
print("   3. Enter credentials above")
print("=" * 60)
