import sys
sys.path.insert(0, '.')

from db_helpers import get_school_budget, save_school_budget
from database import DATABASE_PATH
import sqlite3

school_id = 5
financial_year = '2026-2027'

print("Step 1: Get current budget")
budget = get_school_budget(school_id, financial_year)
print(f"  Items: {len(budget['items'])}")
print(f"  First 3 allocations: {[item['totalAllocation'] for item in budget['items'][:3]]}")

print("\nStep 2: Modify allocations")
for i in range(3):
    budget['items'][i]['totalAllocation'] = 5000.0 * (i + 1)
    budget['items'][i]['monthlyAllocations']['April'] = 500.0 * (i + 1)

print("\nStep 3: Save budget")
result = save_school_budget(school_id, financial_year, budget)
print(f"  Save result: {result}")

print("\nStep 4: Force checkpoint")
conn = sqlite3.connect(DATABASE_PATH)
conn.execute('PRAGMA wal_checkpoint(TRUNCATE)')
conn.close()
print("  Checkpoint complete")

print("\nStep 5: Verify from database directly")
conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()
cursor.execute('''
    SELECT template_row_id, total_allocation
    FROM budget_items
    WHERE school_id = ? AND financial_year = ?
    ORDER BY template_row_id
    LIMIT 3
''', (school_id, financial_year))
rows = cursor.fetchall()
print(f"  Database values: {[row[1] for row in rows]}")
conn.close()

print("\nStep 6: Reload via helper function")
budget2 = get_school_budget(school_id, financial_year)
print(f"  Reloaded values: {[item['totalAllocation'] for item in budget2['items'][:3]]}")

expected = [5000.0, 10000.0, 15000.0]
actual = [item['totalAllocation'] for item in budget2['items'][:3]]

if actual == expected:
    print("\n✓ SUCCESS: Data persists correctly!")
else:
    print(f"\n✗ FAILED: Expected {expected}, got {actual}")
