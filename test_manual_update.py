import sqlite3
import json

conn = sqlite3.connect('data/grant_management.db')
cursor = conn.cursor()

# Test update
school_id = 5
financial_year = '2026-2027'
template_row_id = 1
test_allocation = 50000.0
test_monthly = json.dumps({"April": 5000, "May": 5000, "June": 5000, "July": 5000, "August": 5000, "September": 5000, "October": 5000, "November": 5000, "December": 5000, "January": 5000, "February": 5000, "March": 5000})

print(f"Updating school {school_id}, year {financial_year}, row {template_row_id}")
print(f"Setting allocation to {test_allocation}")

cursor.execute('''
    UPDATE budget_items
    SET total_allocation = ?, monthly_allocations = ?
    WHERE school_id = ? AND financial_year = ? AND template_row_id = ?
''', (test_allocation, test_monthly, school_id, financial_year, template_row_id))

print(f"Rows updated: {cursor.rowcount}")
conn.commit()

# Verify
cursor.execute('''
    SELECT total_allocation, monthly_allocations
    FROM budget_items
    WHERE school_id = ? AND financial_year = ? AND template_row_id = ?
''', (school_id, financial_year, template_row_id))

row = cursor.fetchone()
print(f"\nVerification:")
print(f"  Allocation: {row[0]}")
print(f"  Monthly: {row[1][:50]}...")

conn.close()

if row[0] == test_allocation:
    print("\n✅ UPDATE WORKS - Data persists!")
else:
    print("\n❌ UPDATE FAILED - Data not saved!")
