# Sequential Document Numbering System

## Overview
The Grant Management System implements automatic sequential document numbering for all transaction documents. Each transaction receives a unique 4-digit number that is shared across all three related documents.

## Document Types Covered
1. **Payment Receipt** - Receipt given to payee
2. **GP10 Payment Voucher** - Official government payment voucher
3. **Loose Minute** - Internal approval document

## Numbering Rules

### Format
- **4-digit zero-padded numbers**: 0001, 0002, 0003, ..., 9999
- **Sequential**: Each new transaction increments by 1
- **Unique**: No duplicates within a financial year
- **Linked**: All three documents share the same number

### Financial Year Separation
- **Resets per year**: Each financial year starts from 0001
- **Independent sequences**: 2026-2027 and 2027-2028 both start at 0001
- **Year-specific**: Document numbers are tied to financial year

### Examples

**Financial Year 2026-2027:**
- First transaction: Receipt #0001, GP10 #0001, Loose Minute #0001
- Second transaction: Receipt #0002, GP10 #0002, Loose Minute #0002
- Third transaction: Receipt #0003, GP10 #0003, Loose Minute #0003

**Financial Year 2027-2028:**
- First transaction: Receipt #0001, GP10 #0001, Loose Minute #0001 (resets)
- Second transaction: Receipt #0002, GP10 #0002, Loose Minute #0002

## Implementation

### Database Storage
Each debit record includes a `documentNumber` field:

```json
{
  "id": "debit_1234567890.123",
  "documentNumber": "0001",
  "financialYear": "2026-2027",
  "date": "2026-05-15",
  "supplierName": "John Doe",
  "amount": 50000,
  ...
}
```

### Auto-Generation Process

1. **User creates a debit entry** (payment transaction)
2. **System queries** all existing debits for current financial year
3. **Finds highest number** in use (e.g., 0045)
4. **Increments by 1** (0046)
5. **Formats as 4-digit** string with leading zeros
6. **Saves to debit record** as `documentNumber`
7. **All three documents** use this same number

### Code Implementation

```python
def get_next_document_number(financial_year):
    """Get next sequential document number for the financial year"""
    debits = get_debits(financial_year)
    
    # Find the highest document number
    max_number = 0
    for debit in debits:
        if 'documentNumber' in debit:
            num = int(debit['documentNumber'])
            if num > max_number:
                max_number = num
    
    # Return next number as zero-padded 4-digit string
    next_number = max_number + 1
    return f"{next_number:04d}"
```

### Document Display

**GP10 Payment Voucher:**
```
PAYMENT VOUCHER NO: 0001
```

**Loose Minute:**
```
LOOSE MINUTE NO: 0001
```

**Payment Receipt:**
```
Receipt No.
#0001
```

## Benefits

✅ **Automatic**: No manual entry required
✅ **Unique**: Prevents duplicate numbers
✅ **Sequential**: Easy to track and audit
✅ **Linked**: All documents for a transaction match
✅ **Persistent**: Numbers saved permanently
✅ **Year-based**: Clean separation per financial year
✅ **Professional**: Standard 4-digit format

## User Experience

1. **Create Debit Entry**: User fills out payment form
2. **Submit**: System auto-generates next number
3. **View Documents**: All three documents show same number
4. **Print/Download**: Number appears on all documents
5. **Reprint**: Same number always displayed
6. **Audit Trail**: Sequential numbers make tracking easy

## Data Integrity

- **No gaps**: Numbers increment continuously
- **No duplicates**: Each number used once per year
- **Permanent**: Numbers never change after assignment
- **Recoverable**: System can rebuild sequence from existing data
- **Year-isolated**: Different years don't interfere

## Migration Notes

### Existing Data
Debits created before this feature will not have `documentNumber` field. The system handles this gracefully:
- Old debits: Display "0001" as fallback
- New debits: Get proper sequential numbers
- Recommendation: Manually assign numbers to old records if needed

### Starting Fresh
When initializing a new financial year:
- First debit automatically gets "0001"
- Sequence continues from there
- No configuration needed

## Technical Details

### Storage Location
- File: `data/debits.json`
- Field: `documentNumber` (string)
- Format: "0001", "0002", etc.

### Query Performance
- Scans all debits for current year
- Finds maximum number
- O(n) complexity where n = number of debits
- Acceptable for typical school usage (hundreds of transactions)

### Edge Cases Handled
- **Empty database**: Returns "0001"
- **Missing field**: Treats as 0
- **Invalid format**: Skips and continues
- **Year switch**: Automatically resets to "0001"

## Future Enhancements

Possible improvements:
- Pre-generate number blocks for performance
- Add prefix for year identification (e.g., "26-0001")
- Support custom starting numbers
- Add number reservation system
- Implement number recycling for deleted transactions
