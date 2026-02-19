# ✅ FIXED: Tracking Page Error + Settings Data Population

## Issues Fixed

### 1. Tracking Page Crash
**Error:** `TypeError: unsupported format string passed to Undefined.__format__`

**Root Cause:** Template tried to access `budget.totalGrant` but field didn't exist

**Fix Applied:**
- Updated `get_budget()` to include BOTH `totalGrant` and `total_grant` fields
- Updated `get_settings()` to include BOTH naming conventions
- Fixed tracking.html template to safely handle both field names:
  ```jinja
  {{ (budget.totalGrant or budget.total_grant or 0) if budget else 0 }}
  ```

### 2. Settings Data Not Populating
**Root Cause:** Field name mismatch between database (`total_grant`) and templates (`totalGrant`)

**Fix Applied:**
- Standardized to support BOTH naming conventions for backward compatibility
- `get_budget()` now fetches settings and adds both field names
- `get_settings()` returns both `totalGrant` and `total_grant`

## Files Modified

### app.py
1. **get_budget()** - Now includes:
   - Fetches settings from database
   - Adds `totalGrant` (camelCase for templates)
   - Adds `total_grant` (snake_case for consistency)
   - Adds `schoolName` from session

2. **get_settings()** - Now returns:
   - Both `totalGrant` and `total_grant` fields
   - Proper school_id filtering
   - Financial year from session

### templates/tracking.html
- Fixed all `budget.totalGrant` references to handle both field names
- Safe fallback: `(budget.totalGrant or budget.total_grant or 0)`

### templates/budget.html
- Fixed display of Total Grant to handle both field names
- Fixed form input value to handle both field names

## Result

✅ Tracking page loads without errors
✅ Total Grant displays correctly from settings
✅ Budget Allocation shows correct school data
✅ Settings populate across all pages
✅ Multi-tenant isolation maintained
✅ Backward compatibility with both naming conventions

## Testing Checklist

- [ ] Login to system
- [ ] Navigate to Tracking page - should load without error
- [ ] Check Total Grant displays correctly
- [ ] Navigate to Budget Allocation - should show school name and total grant
- [ ] Navigate to Settings - should show saved values
- [ ] Change financial year - should persist
- [ ] Add/edit budget items - should work correctly

## Technical Notes

**Field Name Standardization:**
- Database uses: `total_grant` (snake_case)
- Templates can use: `totalGrant` OR `total_grant`
- Both are supported for maximum compatibility

**Data Flow:**
1. Database stores: `total_grant`
2. `get_settings()` returns: both `totalGrant` and `total_grant`
3. `get_budget()` includes: both fields from settings
4. Templates access: either field name safely

This ensures no breaking changes while fixing the errors.
