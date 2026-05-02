import sqlite3
import os

DATABASE_PATH = r'd:\2025-2026\PRODUCTION\USA\RN-LAB-TECH Grant Management System\data\grant_management.db'

def migrate():
    print(f"Connecting to {DATABASE_PATH}...")
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    columns = [
        ('ipdc_venue', 'TEXT'),
        ('ipdc_minute_no', 'TEXT'),
        ('ipdc_members', 'TEXT'),
        ('ipdc_opening_prayer', 'TEXT'),
        ('ipdc_closing_prayer', 'TEXT'),
        ('ipdc_quotations', 'TEXT')
    ]
    
    for col_name, col_type in columns:
        try:
            cursor.execute(f'ALTER TABLE debits ADD COLUMN {col_name} {col_type}')
            print(f"✅ Added {col_name}")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print(f"ℹ️ {col_name} already exists")
            else:
                print(f"❌ Error adding {col_name}: {e}")
                
    conn.commit()
    conn.close()
    print("Migration complete.")

if __name__ == "__main__":
    migrate()
