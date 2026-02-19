import sqlite3

conn = sqlite3.connect('data/grant_management.db')
cursor = conn.cursor()

cursor.execute('''
    SELECT school_id, template_row_id, total_allocation, 
           substr(monthly_allocations, 1, 100) as monthly_sample
    FROM budget_items
    WHERE total_allocation > 0
    LIMIT 10
''')

rows = cursor.fetchall()

if rows:
    print(f"Found {len(rows)} rows with allocations:")
    for row in rows:
        print(f"  School {row[0]}, Row {row[1]}: {row[2]}")
else:
    print("No budget allocations found (all are 0)")
    print("\nThis confirms budget data is NOT being saved.")
    print("\nPlease:")
    print("1. Go to Budget Allocation page")
    print("2. Enter a value (e.g., 10000) in ANY Annual Allocation field")
    print("3. Click 'Save All Changes'")
    print("4. Check browser console for errors (F12)")
    print("5. Run this script again")

conn.close()
