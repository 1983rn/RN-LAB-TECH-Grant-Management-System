import os
import sqlite3
import glob

print("=== DATABASE LOCATION VERIFICATION ===\n")

# Check from database.py
from database import DATABASE_PATH
print(f"1. Database path from database.py:")
print(f"   {DATABASE_PATH}")
print(f"   Exists: {os.path.exists(DATABASE_PATH)}")
if os.path.exists(DATABASE_PATH):
    print(f"   Size: {os.path.getsize(DATABASE_PATH):,} bytes")

# Search for all .db files
print(f"\n2. Searching for all .db files in project:")
db_files = glob.glob("**/*.db", recursive=True)
for db_file in db_files:
    abs_path = os.path.abspath(db_file)
    size = os.path.getsize(db_file)
    print(f"   Found: {abs_path} ({size:,} bytes)")

if len(db_files) > 1:
    print(f"\n   WARNING: Multiple database files found!")
    print(f"   This causes data loss - only one should exist")
else:
    print(f"\n   OK: Only one database file found")

# Check data in database
print(f"\n3. Checking data in database:")
try:
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM schools WHERE school_name != 'DEVELOPER_ACCOUNT'")
    schools = cursor.fetchone()[0]
    print(f"   Schools: {schools}")
    
    cursor.execute("SELECT COUNT(*) FROM budget_items WHERE total_allocation > 0")
    budget_with_data = cursor.fetchone()[0]
    print(f"   Budget items with allocations: {budget_with_data}")
    
    cursor.execute("SELECT COUNT(*) FROM credits")
    credits = cursor.fetchone()[0]
    print(f"   Credits: {credits}")
    
    cursor.execute("SELECT COUNT(*) FROM debits")
    debits = cursor.fetchone()[0]
    print(f"   Debits: {debits}")
    
    conn.close()
    
    if budget_with_data > 0 or credits > 0 or debits > 0:
        print(f"\n   OK: Database contains data")
    else:
        print(f"\n   WARNING: Database exists but has no transaction data")
        
except Exception as e:
    print(f"   ERROR: {e}")

print(f"\n=== VERIFICATION COMPLETE ===")
