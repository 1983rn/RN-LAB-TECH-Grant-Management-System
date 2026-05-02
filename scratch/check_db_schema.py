import sqlite3
import os

DB_PATH = r'D:\2025-2026\PRODUCTION\USA\RN-LAB-TECH Grant Management System\data\grant_management.db'

def check_schema():
    if not os.path.exists(DB_PATH):
        print(f"ERROR: Database not found at {DB_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print(f"Checking table 'debits'...")
    cursor.execute("PRAGMA table_info(debits)")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  Column: {col[1]} ({col[2]})")
    
    column_names = [col[1] for col in columns]
    if 'ipdc_quotations' in column_names:
        print("✅ Column 'ipdc_quotations' EXISTS")
    else:
        print("❌ Column 'ipdc_quotations' MISSING")
    
    conn.close()

if __name__ == '__main__':
    check_schema()
