# POW Auto-Initialization Fix

## Problem
When selecting a new financial year:
- ❌ Budget Allocation page showed empty POWs
- ❌ Credit Register showed no POWs
- ❌ Debit Register showed no POWs
- ❌ System did not auto-initialize structure

## Root Cause
The system changed the financial year in session but did NOT create the budget structure (42 template rows across 16 POWs) for the new year.

## Solution Implemented

### 1. Created `initialize_budget_for_year()` function in `db_helpers.py`
```python
def initialize_budget_for_year(school_id, financial_year):
    """Auto-initialize budget structure for new financial year if not exists"""
    # Check if budget items already exist
    # If not, insert all 42 template rows with zero allocations
```

### 2. Auto-initialization on budget access
Modified `get_budget()` in `app.py` to automatically initialize:
```python
def get_budget(financial_year):
    school_id = get_current_school_id()
    # Auto-initialize budget structure if not exists
    initialize_budget_for_year(school_id, financial_year)
    # Then load budget
```

### 3. Explicit initialization on financial year change
In `/settings` route when financial year changes:
```python
if form_type == 'financial_year':
    session['financial_year'] = financial_year
    initialize_budget_for_year(school_id, financial_year)
```

## How It Works

### Initialization Logic:
1. **Check:** Query if budget_items exist for (school_id, financial_year)
2. **Skip:** If rows exist (count > 0), do nothing
3. **Create:** If no rows, insert all 42 template rows with:
   - All 16 POWs
   - All sub-activities
   - All budget codes
   - Zero allocations
   - Empty monthly allocations

### Data Isolation:
- ✅ Each school has separate budget rows
- ✅ Each financial year has separate budget rows
- ✅ UNIQUE constraint: (school_id, financial_year, template_row_id)
- ✅ No cross-contamination of data

## Result

### When New Financial Year Selected:
1. User changes financial year in Settings
2. System calls `initialize_budget_for_year()`
3. Function checks if budget exists
4. If not, creates all 42 template rows
5. User navigates to any page
6. All POWs are populated and ready

### Automatic Initialization:
- Budget Allocation page → Auto-initializes on load
- Credit Register → Sees all POWs (from budget_items)
- Debit Register → Sees all POWs (from budget_items)

## Testing

### Test New Financial Year:
1. Login to application
2. Go to Settings
3. Change financial year to "2027-2028"
4. Click Save
5. Go to Budget Allocation → Should show all 42 rows
6. Go to Credit Register → Dropdown should show all POWs
7. Go to Debit Register → Dropdown should show all POWs

### Test Existing Financial Year:
1. Change back to "2026-2027"
2. All previous data should still be there
3. No data loss
4. No duplicate rows

## Files Modified

1. **db_helpers.py** - Added `initialize_budget_for_year()` function
2. **app.py** - Modified `get_budget()` to auto-initialize
3. **app.py** - Settings route already calls initialization

## Benefits

✅ **Automatic** - No manual initialization needed
✅ **Safe** - Only creates if not exists (no duplicates)
✅ **Isolated** - Per school, per year
✅ **Seamless** - Works transparently
✅ **Persistent** - Survives restarts
✅ **Multi-tenant** - Each school independent

## No Migration Needed

The fix works immediately:
- Existing data remains intact
- New years auto-initialize on first access
- No database schema changes required
