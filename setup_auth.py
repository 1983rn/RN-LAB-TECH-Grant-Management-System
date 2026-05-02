#!/usr/bin/env python3
"""
Setup Authentication System
Creates default school account and developer account
"""
from database import init_database, create_developer_account, get_db, hash_password

def create_default_school():
    """Create default school account"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM schools WHERE username = ?', ('admin',))
        if not cursor.fetchone():
            password_hash = hash_password('admin123')
            cursor.execute('''
                INSERT INTO schools (school_name, username, password_hash, is_active, subscription_status)
                VALUES (?, ?, ?, ?, ?)
            ''', ('Default School', 'admin', password_hash, 1, 'PAID'))
            print("✅ Default school account created (admin/admin123)")
        else:
            print("ℹ️  Default school account already exists")

if __name__ == '__main__':
    print("🔧 Setting up authentication system...")
    init_database()
    create_developer_account()
    create_default_school()
    print("\n✅ Setup complete!")
    print("\n🔐 Login Credentials:")
    print("   School Admin: admin / admin123")
    print("   Developer: juniornsambe@yahoo.com / blessings19831983/")
    print("   (Type 'devaccess' on login screen for developer mode)")
