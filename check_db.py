import sqlite3
import os

DATABASE_PATH = r'd:\2025-2026\PRODUCTION\USA\RN-LAB-TECH Grant Management System\data\grant_management.db'

def check_columns():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(debits)")
    columns = [row[1] for row in cursor.fetchall()]
    print("Columns in 'debits' table:")
    for col in columns:
        print(f" - {col}")
    conn.close()

if __name__ == "__main__":
    check_columns()
