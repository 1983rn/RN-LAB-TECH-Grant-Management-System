# Budget Allocation Data Persistence Fix

## Problem
Budget allocation data was not being saved properly. After entering data and logging out, only the "Grant Total" remained - all budget item allocations were lost.

## Root Cause
The `save_school_budget()` function in `db_helpers.py` was using `UPDATE` statements only. This approach failed because:
1. When UPDATE doesn't find matching rows, it silently does nothing
2. The function had no fallback to INSERT new rows
3. Data appeared to save successfully but was never actually written to the database

## Solution
Changed the save logic from `UPDATE` to `INSERT OR REPLACE`:

**Before:**
```python
cursor.execute('''
    UPDATE budget_items
    SET total_allocation = ?, monthly_allocations = ?
    WHERE school_id = ? AND financial_year = ? AND template_row_id = ?
''', (...))
```

**After:**
```python
cursor.execute('''
    INSERT OR REPLACE INTO budget_items
    (school_id, financial_year, template_row_id, item_key, pow_no, pow_name, 
     sub_activity, sub_item_description, code, total_allocation, monthly_allocations)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (...))
```

## Why This Works
- `INSERT OR REPLACE` is SQLite's UPSERT operation
- If a row with matching `(school_id, financial_year, template_row_id)` exists, it updates it
- If no matching row exists, it inserts a new one
- The database has a `UNIQUE(school_id, financial_year, template_row_id)` constraint that makes this work correctly

## Files Modified
- `db_helpers.py` - Updated `save_school_budget()` function

## Testing
1. Login to the application
2. Navigate to Budget Allocation page
3. Enter values in "Annual Allocation" and monthly columns
4. Click "Save All Changes"
5. Logout and login again
6. Verify all entered data is still present

## Additional Notes
- The "Grant Total" was always saved because it's stored in a different table (`school_settings`)
- Budget items are stored in the `budget_items` table with a unique constraint
- The fix ensures data persistence across sessions without data loss
