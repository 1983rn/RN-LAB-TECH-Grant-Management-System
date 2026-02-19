# Master Template Implementation - POW Budget Structure

## Overview
The system now uses a **master template** approach where every school gets an exact copy of 42 predefined budget rows across 16 POWs (Program of Works).

## Key Changes

### 1. Master Template (42 Rows)
- **Location**: `app.py` → `generate_budget_structure()`
- **Structure**: 42 rows across 16 POWs
- **Uniqueness**: Each row has a `template_row_id` (1-42)

### 2. Database Schema
- **New Column**: `template_row_id INTEGER NOT NULL`
- **Unique Constraint**: `UNIQUE(school_id, financial_year, template_row_id)`
- **Protection**: Prevents any duplicate rows per school

### 3. Row Distribution
```
POW 1:  14 rows (Facilitating office operations)
POW 2:   1 row  (Management of examinations)
POW 3:   2 rows (Budget meetings)
POW 4:   2 rows (SMASSE)
POW 5:   3 rows (Sporting activities)
POW 6:   1 row  (Special needs education)
POW 7:   3 rows (Teaching materials)
POW 8:   2 rows (HIV/AIDS & first aid)
POW 9:   2 rows (Infrastructure maintenance)
POW 10:  2 rows (COSOMA & Computer Service)
POW 11:  3 rows (Teacher training)
POW 12:  2 rows (Payment vouchers)
POW 13:  1 row  (Sanitary pads)
POW 14:  1 row  (PPEs)
POW 15:  1 row  (Boarding expenses)
POW 16:  2 rows (Education visits)
---
TOTAL:  42 rows
```

## How It Works

### School Registration
When a new school is registered:
1. System copies all 42 rows from master template
2. Each row gets `template_row_id` (1-42)
3. Database enforces uniqueness per school
4. **No duplicates possible**

### Financial Year Activation
When a school activates a new financial year:
1. System copies all 42 rows for that year
2. Same `template_row_id` values (1-42)
3. Separate data per financial year
4. **Complete isolation**

### Data Integrity
- **Uniqueness**: `(school_id, financial_year, template_row_id)` must be unique
- **Immutability**: Template rows are never deleted
- **Isolation**: Each school's data is completely separate
- **No self-healing**: System doesn't auto-add/remove rows

## Migration

### Script: `migrate_template_row_id.py`
1. Backs up existing data
2. Drops old table
3. Creates new table with `template_row_id`
4. Clears all budget data
5. Reinitializes all schools with master template

### Startup: `Start_Application.bat`
- Runs migration automatically on startup
- Ensures all schools have correct structure
- Safe to run multiple times (idempotent)

## Benefits

✅ **No Duplicates**: Database constraint prevents duplicates
✅ **No Missing Rows**: Every school gets all 42 rows
✅ **No Data Leakage**: Complete school_id isolation
✅ **Predictable Structure**: Same 42 rows for every school
✅ **Easy Maintenance**: Single master template to update

## Code Locations

- **Master Template**: `app.py` → `generate_budget_structure()`
- **Database Schema**: `database.py` → `init_database()`
- **Migration Script**: `migrate_template_row_id.py`
- **School Creation**: `app.py` → `dev_add_school()`
- **Budget Route**: `app.py` → `budget()` (no self-healing)

## Testing

```bash
# Verify all schools have 42 rows
python -c "import sqlite3; conn = sqlite3.connect('data/grant_management.db'); cursor = conn.cursor(); cursor.execute('SELECT school_id, COUNT(*) FROM budget_items GROUP BY school_id'); [print(f'School {r[0]}: {r[1]} rows') for r in cursor.fetchall()]"

# Verify no duplicates
python -c "import sqlite3; conn = sqlite3.connect('data/grant_management.db'); cursor = conn.cursor(); cursor.execute('SELECT school_id, financial_year, template_row_id, COUNT(*) as cnt FROM budget_items GROUP BY school_id, financial_year, template_row_id HAVING cnt > 1'); print('Duplicates:', cursor.fetchall())"
```

## Current Status

✅ All schools have exactly 42 budget rows
✅ No duplicates exist
✅ Unique constraint enforced
✅ NANJATI CDSS recreated with proper structure
✅ Migration runs on startup
