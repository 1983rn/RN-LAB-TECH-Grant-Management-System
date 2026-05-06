import sqlite3
import os

db_paths = [
    r'd:\2025-2026\PRODUCTION\USA\RN-LAB-TECH Grant Management System\grant_management.db',
    r'd:\2025-2026\PRODUCTION\USA\RN-LAB-TECH Grant Management System\data\grant_management.db'
]

for path in db_paths:
    if os.path.exists(path):
        print(f"Checking {path}...")
        try:
            conn = sqlite3.connect(path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT id, school_name, username FROM schools")
            rows = cursor.fetchall()
            if not rows:
                print("  No schools found.")
            for row in rows:
                print(f"  ID: {row['id']}, Name: {row['school_name']}, Username: {row['username']}")
            conn.close()
        except Exception as e:
            print(f"  Error: {e}")
    else:
        print(f"{path} does not exist.")
