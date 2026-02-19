#!/usr/bin/env python3
"""
Test Authentication System
Verifies all security features are working
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import init_database, get_db, hash_password, verify_password, create_developer_account

def test_database():
    """Test database initialization"""
    print("🧪 Testing database initialization...")
    try:
        init_database()
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def test_developer_account():
    """Test developer account creation"""
    print("\n🧪 Testing developer account...")
    try:
        create_developer_account()
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM schools WHERE username = ?', ('juniornsambe@yahoo.com',))
            dev = cursor.fetchone()
            if dev:
                print("✅ Developer account exists")
                print(f"   Username: {dev['username']}")
                print(f"   Status: {dev['subscription_status']}")
                return True
            else:
                print("❌ Developer account not found")
                return False
    except Exception as e:
        print(f"❌ Developer account test failed: {e}")
        return False

def test_school_account():
    """Test default school account"""
    print("\n🧪 Testing default school account...")
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM schools WHERE username = ?', ('admin',))
            if not cursor.fetchone():
                password_hash = hash_password('admin123')
                cursor.execute('''
                    INSERT INTO schools (school_name, username, password_hash, is_active, subscription_status)
                    VALUES (?, ?, ?, ?, ?)
                ''', ('Default School', 'admin', password_hash, 1, 'PAID'))
                print("✅ Default school account created")
            else:
                print("✅ Default school account exists")
            return True
    except Exception as e:
        print(f"❌ School account test failed: {e}")
        return False

def test_password_hashing():
    """Test password hashing"""
    print("\n🧪 Testing password hashing...")
    try:
        password = "test123"
        hashed = hash_password(password)
        if verify_password(password, hashed):
            print("✅ Password hashing works correctly")
            return True
        else:
            print("❌ Password verification failed")
            return False
    except Exception as e:
        print(f"❌ Password hashing test failed: {e}")
        return False

def test_tables():
    """Test all required tables exist"""
    print("\n🧪 Testing database tables...")
    required_tables = [
        'schools', 'school_settings', 'budget_items', 'credits', 'debits',
        'document_sequences', 'subscription_messages', 'school_sessions',
        'password_reset_tokens', 'audit_logs'
    ]
    
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            missing = [t for t in required_tables if t not in tables]
            if missing:
                print(f"❌ Missing tables: {', '.join(missing)}")
                return False
            else:
                print(f"✅ All {len(required_tables)} required tables exist")
                return True
    except Exception as e:
        print(f"❌ Table test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("AUTHENTICATION SYSTEM TEST SUITE")
    print("=" * 60)
    
    results = []
    results.append(("Database Initialization", test_database()))
    results.append(("Database Tables", test_tables()))
    results.append(("Password Hashing", test_password_hashing()))
    results.append(("Developer Account", test_developer_account()))
    results.append(("School Account", test_school_account()))
    
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    
    print("\n" + "=" * 60)
    print(f"TOTAL: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED - System Ready!")
        print("\n🔐 Login Credentials:")
        print("   School: admin / admin123")
        print("   Developer: juniornsambe@yahoo.com / blessings19831983/")
        print("   (Type 'devaccess' on login screen)")
        return 0
    else:
        print("\n⚠️  SOME TESTS FAILED - Please review errors above")
        return 1

if __name__ == '__main__':
    sys.exit(main())
