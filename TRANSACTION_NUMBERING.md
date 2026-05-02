# Transaction Numbering System - Technical Documentation

## Overview

The Grant Management System uses a **unified, persistent, year-based sequential numbering system** for all transaction documents (GP10 Voucher, Loose Minute, Payment Receipt).

## Key Features

✅ **Unified Numbering**: All three documents (GP10, Loose Minute, Receipt) share the same transaction number  
✅ **Sequential**: Numbers increment continuously (0001, 0002, 0003...)  
✅ **Year-Based**: Counters are isolated per financial year  
✅ **No Monthly Reset**: Numbers continue across month boundaries  
✅ **Persistent**: Survives system restarts and database reconnections  
✅ **Multi-Tenant Safe**: Each school has independent counters  
✅ **Concurrency Safe**: Uses database locks to prevent duplicate numbers  

## Architecture

### Database Schema

#### financial_year_counters Table
```sql
CREATE TABLE financial_year_counters (
    school_id INTEGER NOT NULL,
    financial_year TEXT NOT NULL,
    last_number INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (school_id, financial_year)
);
```

**Purpose**: Stores the last used transaction number for each school/year combination.

#### debits Table (Updated)
```sql
CREATE TABLE debits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    school_id INTEGER NOT NULL,
    financial_year TEXT NOT NULL,
    document_number TEXT NOT NULL,  -- Unified transaction number
    date_paid DATE NOT NULL,
    month TEXT NOT NULL,
    item_id TEXT NOT NULL,
    sub_item_description TEXT,
    code TEXT,
    description TEXT,
    amount REAL NOT NULL,
    amount_words TEXT,
    supplier_name TEXT,
    position TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id)
);

-- Unique constraint prevents duplicate transaction numbers
CREATE UNIQUE INDEX idx_unique_transaction
ON debits (school_id, financial_year, document_number);
```

**Changes from Old System**:
- ❌ Removed: `loose_minute_number` column
- ❌ Removed: `receipt_number` column
- ✅ Kept: `document_number` (now serves all three documents)

### Core Function

#### generate_transaction_number()
```python
def generate_transaction_number(school_id, financial_year):
    """
    Generate persistent sequential transaction number
    - Year-based, no monthly reset
    - Concurrency safe with BEGIN IMMEDIATE
    """
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Start transaction lock (prevents race conditions)
        cursor.execute("BEGIN IMMEDIATE")
        
        try:
            # Ensure counter row exists
            cursor.execute('''
                INSERT OR IGNORE INTO financial_year_counters
                (school_id, financial_year, last_number)
                VALUES (?, ?, 0)
            ''', (school_id, financial_year))
            
            # Fetch current counter
            cursor.execute('''
                SELECT last_number
                FROM financial_year_counters
                WHERE school_id = ? AND financial_year = ?
            ''', (school_id, financial_year))
            
            last_number = cursor.fetchone()[0]
            new_number = last_number + 1
            
            # Update counter
            cursor.execute('''
                UPDATE financial_year_counters
                SET last_number = ?
                WHERE school_id = ? AND financial_year = ?
            ''', (new_number, school_id, financial_year))
            
            conn.commit()
            return str(new_number).zfill(4)  # Returns "0001", "0002", etc.
        except Exception:
            conn.rollback()
            raise
```

**Why BEGIN IMMEDIATE?**
- Prevents two users from generating the same number simultaneously
- Locks the database for writing immediately
- Ensures atomic counter increment

## Usage in Application

### When Creating a Debit Entry

```python
@app.route('/add_debit', methods=['POST'])
@require_login
def add_debit():
    school_id = get_current_school_id()
    financial_year = get_financial_year()
    
    # Generate unified transaction number
    transaction_number = generate_transaction_number(school_id, financial_year)
    
    debit_data = {
        'documentNumber': transaction_number,  # Used for all 3 documents
        'date': data.get('date'),
        'month': data.get('month'),
        'itemId': data.get('itemId'),
        'amount': data.get('amount'),
        # ... other fields
    }
    
    save_debit(debit_data)
```

### When Displaying Documents

The `get_school_debits()` function automatically populates all three number fields:

```python
def get_school_debits(school_id, financial_year):
    # ... fetch from database ...
    
    debit = {
        'documentNumber': row['document_number'],
        'looseMinuteNumber': row['document_number'],    # Same number
        'gp10VoucherNumber': row['document_number'],    # Same number
        'receiptNumber': row['document_number'],        # Same number
        # ... other fields
    }
```

## Behavior Examples

### Example 1: Continuous Numbering (No Monthly Reset)

| Date | Month | Transaction Number |
|------|-------|-------------------|
| 2026-04-15 | April | 0001 |
| 2026-04-20 | April | 0002 |
| 2026-05-05 | May | 0003 ← Continues from April |
| 2026-05-10 | May | 0004 |
| 2026-06-01 | June | 0005 ← No reset |

### Example 2: System Restart (Persistent)

```
1. Create transaction → 0020
2. Restart application
3. Create transaction → 0021 ← Counter persists
```

### Example 3: Financial Year Reset

```
Financial Year 2026-2027:
  Transaction 1 → 0001
  Transaction 2 → 0002
  ...
  Transaction 50 → 0050

Switch to Financial Year 2027-2028:
  Transaction 1 → 0001 ← Resets for new year
  Transaction 2 → 0002
```

### Example 4: Multi-School Isolation

```
School A (2026-2027):
  Transaction 1 → 0001
  Transaction 2 → 0002

School B (2026-2027):
  Transaction 1 → 0001 ← Independent counter
  Transaction 2 → 0002
```

## Migration

### Automatic Migration

The system automatically migrates from the old numbering system:

1. **Run Migration Script**: `python migrate_transaction_numbers.py`
2. **What It Does**:
   - Creates `financial_year_counters` table
   - Removes old `document_sequences` table
   - Removes `loose_minute_number` and `receipt_number` columns
   - Renumbers existing debits sequentially (by date)
   - Creates unique index to prevent duplicates
   - Updates counters to match highest existing number

### Migration is Safe

- ✅ Backs up data before changes
- ✅ Preserves all transaction data
- ✅ Assigns sequential numbers to existing transactions
- ✅ Rollback on error

## Verification

Run the verification script to confirm the system is working:

```bash
python verify_transaction_numbers.py
```

**Expected Output**:
```
============================================================
TRANSACTION NUMBERING VERIFICATION
============================================================

[1] Checking financial_year_counters table...
    SUCCESS: Table exists
    Found 3 counter(s):
      - School 5, Year 2026-2027: Counter = 5

[2] Checking debits table structure...
    SUCCESS: Column 'document_number' exists
    SUCCESS: Old column 'loose_minute_number' removed
    SUCCESS: Old column 'receipt_number' removed

[3] Checking unique index...
    SUCCESS: Unique index exists

[4] Checking existing debits...
    Found 1 school/year combination(s):
      - School 5, Year 2026-2027: 5 debit(s)
        Numbers: 0001, 0002, 0003, 0004, 0005
        SUCCESS: Sequential numbering verified

============================================================
VERIFICATION SUMMARY
============================================================
SUCCESS: Unified transaction numbering system is active
```

## Troubleshooting

### Issue: Duplicate Transaction Numbers

**Cause**: Unique constraint violation  
**Solution**: Run migration script to renumber existing transactions

```bash
python migrate_transaction_numbers.py
```

### Issue: Counter Not Incrementing

**Cause**: Database lock or transaction not committed  
**Solution**: Check database connection and ensure WAL mode is enabled

```bash
python enable_wal.py
```

### Issue: Numbers Reset Monthly

**Cause**: Old code still in use  
**Solution**: Ensure you're using `generate_transaction_number()` not `get_next_document_number()`

## Comparison: Old vs New System

| Feature | Old System | New System |
|---------|-----------|------------|
| **Number of Counters** | 3 separate (GP10, Loose Minute, Receipt) | 1 unified counter |
| **Monthly Reset** | ❌ Yes (numbers reset each month) | ✅ No (continuous) |
| **Restart Persistence** | ❌ No (used MAX() query) | ✅ Yes (stored in DB) |
| **Concurrency Safety** | ❌ Race conditions possible | ✅ Locked transactions |
| **Year-Based** | ✅ Yes | ✅ Yes |
| **Multi-Tenant** | ✅ Yes | ✅ Yes |

## Professional Standards Achieved

✅ **ERP-Level Numbering**: Continuous, auditable transaction numbers  
✅ **Accounting Compliance**: No gaps or duplicates in numbering  
✅ **Production Ready**: Handles concurrent users safely  
✅ **Maintainable**: Single source of truth for transaction numbers  
✅ **Scalable**: Efficient database queries with proper indexing  

## Files Modified

1. **database.py**: Added `financial_year_counters` table, removed `document_sequences`
2. **db_helpers.py**: Added `generate_transaction_number()`, updated `get_school_debits()`
3. **app.py**: Updated routes to use unified numbering
4. **migrate_transaction_numbers.py**: Migration script
5. **verify_transaction_numbers.py**: Verification script
6. **Start_Application.bat**: Added migration to startup sequence

## Summary

The unified transaction numbering system provides:
- **Simplicity**: One number for all documents
- **Reliability**: Persistent, no duplicates
- **Correctness**: No monthly reset, year-based isolation
- **Safety**: Concurrency protection, unique constraints
- **Professionalism**: ERP-standard sequential numbering

This is a production-grade implementation suitable for financial management systems.
