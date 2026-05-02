#!/usr/bin/env python3
"""
Diagnose Developer Login Issue
"""
from database import get_db, hash_password, verify_password

print("=" * 60)
print("DEVELOPER LOGIN DIAGNOSTIC")
print("=" * 60)

# Check if database exists
import os
if not os.path.exists('data/grant_management.db'):
    print("❌ Database does not exist!")
    print("   Run: python setup_auth.py")
    exit(1)

print("\n1. Checking developer account in database...")
with get_db() as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM schools WHERE username = ?', ('juniornsambe@yahoo.com',))
    dev = cursor.fetchone()
    
    if not dev:
        print("❌ Developer account NOT FOUND in database!")
        print("   Creating developer account now...")
        from database import create_developer_account
        create_developer_account()
        
        # Check again
        cursor.execute('SELECT * FROM schools WHERE username = ?', ('juniornsambe@yahoo.com',))
        dev = cursor.fetchone()
    
    if dev:
        print("✅ Developer account found:")
        print(f"   ID: {dev['id']}")
        print(f"   Username: {dev['username']}")
        print(f"   School Name: {dev['school_name']}")
        print(f"   Is Active: {dev['is_active']}")
        print(f"   Is Locked: {dev['is_locked']}")
        print(f"   Subscription: {dev['subscription_status']}")
        print(f"   Password Hash: {dev['password_hash'][:20]}...")
        
        print("\n2. Testing password verification...")
        test_password = 'blessings19831983/'
        stored_hash = dev['password_hash']
        
        # Test hash generation
        generated_hash = hash_password(test_password)
        print(f"   Generated hash: {generated_hash[:20]}...")
        print(f"   Stored hash:    {stored_hash[:20]}...")
        
        if generated_hash == stored_hash:
            print("✅ Password hashes MATCH")
        else:
            print("❌ Password hashes DO NOT MATCH")
            print("   Fixing password hash...")
            cursor.execute('UPDATE schools SET password_hash = ? WHERE username = ?',
                         (generated_hash, 'juniornsambe@yahoo.com'))
            conn.commit()
            print("✅ Password hash fixed!")
        
        # Test verify_password function
        if verify_password(test_password, stored_hash):
            print("✅ verify_password() function works correctly")
        else:
            print("❌ verify_password() function failed")
            
        print("\n3. Testing login logic...")
        username = 'juniornsambe@yahoo.com'
        password = 'blessings19831983/'
        
        # Simulate login_developer logic
        if username != 'juniornsambe@yahoo.com':
            print("❌ Username check failed")
        else:
            print("✅ Username check passed")
        
        cursor.execute('''
            SELECT id, password_hash FROM schools 
            WHERE username = ? AND school_name = 'DEVELOPER_ACCOUNT'
        ''', (username,))
        dev_check = cursor.fetchone()
        
        if not dev_check:
            print("❌ Developer account query failed")
        else:
            print("✅ Developer account query succeeded")
            if verify_password(password, dev_check['password_hash']):
                print("✅ Password verification succeeded")
                print("\n" + "=" * 60)
                print("✅ DEVELOPER LOGIN SHOULD WORK!")
                print("=" * 60)
            else:
                print("❌ Password verification failed")
    else:
        print("❌ Could not create developer account")

print("\n" + "=" * 60)
print("DIAGNOSTIC COMPLETE")
print("=" * 60)
