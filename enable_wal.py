#!/usr/bin/env python3
"""
Enable WAL Mode on Existing Database
Fixes SQLite locking issues
"""
import sqlite3
import os
from database import DATABASE_PATH

if not os.path.exists(DATABASE_PATH):
    print("❌ Database not found")
    exit(1)

print("🔧 Enabling WAL mode on database...")

conn = sqlite3.connect(DATABASE_PATH, timeout=10.0)
cursor = conn.cursor()

# Enable WAL mode
cursor.execute('PRAGMA journal_mode=WAL')
result = cursor.fetchone()
print(f"✅ Journal mode: {result[0]}")

# Set synchronous mode
cursor.execute('PRAGMA synchronous=NORMAL')
print("✅ Synchronous mode: NORMAL")

# Set busy timeout
cursor.execute('PRAGMA busy_timeout=10000')
print("✅ Busy timeout: 10000ms")

conn.commit()
conn.close()

print("\n✅ Database optimized for concurrent access!")
print("   - WAL mode enabled (reduces locking)")
print("   - Busy timeout set (waits instead of failing)")
print("   - Synchronous mode optimized")
