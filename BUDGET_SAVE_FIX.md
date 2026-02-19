# Budget Save Error Fix

## Problem
Error when saving budget: "Unexpected token '<'" - Frontend receiving HTML instead of JSON

## Root Cause
The `save_school_budget()` function in `db_helpers.py` was:
1. Using DELETE + INSERT pattern (destroying template rows)
2. Missing `template_row_id` in INSERT statement
3. Causing unique constraint violations

## Solution

### Changed: `db_helpers.py` → `save_school_budget()`
**Before**: DELETE all rows, then INSERT new ones
```python
DELETE FROM budget_items WHERE school_id = ? AND financial_year = ?
INSERT INTO budget_items (...) VALUES (...)  # Missing template_row_id
```

**After**: UPDATE existing rows only
```python
UPDATE budget_items
SET total_allocation = ?, monthly_allocations = ?
WHERE school_id = ? AND financial_year = ? AND template_row_id = ?
```

### Changed: `db_helpers.py` → `get_school_budget()`
- Added `template_row_id` to returned items
- Added `ORDER BY template_row_id` for consistent ordering

## Benefits
✅ Never deletes template rows
✅ Updates allocations in-place
✅ Preserves template structure
✅ No unique constraint violations
✅ Faster (UPDATE vs DELETE+INSERT)

## Testing
```bash
python test_budget_save.py
```
Result: [SUCCESS] Budget save works correctly!

## Status
✅ Fixed and tested
✅ All schools can now save budget allocations
✅ Template structure preserved
