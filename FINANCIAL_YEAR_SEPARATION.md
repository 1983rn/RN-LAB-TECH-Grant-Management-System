# Financial Year Data Separation - Implementation Summary

## Overview
The Grant Management System implements complete financial year data separation. Each financial year operates as an independent workspace while preserving all historical data.

## How It Works

### 1. Global Financial Year Setting
- **Location**: Settings page (top section)
- **Storage**: `data/settings.json` → `financialYear` field
- **Default**: "2026-2027"
- **Function**: `get_financial_year()` retrieves the active year globally

### 2. Data Filtering by Financial Year

All database queries filter by `financialYear` field:

#### Budgets (`data/budgets.json`)
```python
def get_budget(financial_year):
    budgets = read_json_file('budgets.json')
    for budget_item in budgets:
        if budget_item.get('financialYear') == financial_year:
            return budget_item
    return None
```

#### Credits (`data/credits.json`)
```python
def get_credits(financial_year):
    credits = read_json_file('credits.json')
    return [c for c in credits if c.get('financialYear') == financial_year]
```

#### Debits (`data/debits.json`)
```python
def get_debits(financial_year):
    debits = read_json_file('debits.json')
    return [d for d in debits if d.get('financialYear') == financial_year]
```

### 3. Pages Using Financial Year Filter

All routes use `get_financial_year()` instead of query parameters:

- **Home** (`/`) - Welcome page (no data)
- **Settings** (`/settings`) - Displays current year, allows switching
- **Grant Summary** (`/grant-summary`) - Dashboard filtered by year
- **Budget Allocation** (`/budget`) - Budget for selected year only
- **Credit Register** (`/credits`) - Credits for selected year only
- **Debit Register** (`/debits`) - Debits for selected year only
- **Spending Tracking** (`/tracking`) - Spending analysis for selected year
- **Initialize Budget** (`/initialize_budget`) - Creates budget for current year
- **Documents** (`/gp10`, `/loose_minute`, `/receipt`) - Generated for selected year

### 4. Switching Financial Years

**Process:**
1. User goes to Settings
2. Selects new year from dropdown (2026-2031)
3. Form auto-submits
4. System updates `settings.json` → `financialYear`
5. Settings page reloads with notification
6. All other pages automatically use new year on next visit

**Result:**
- New year shows empty pages (no budget, no credits, no debits)
- Old year data remains in JSON files
- Switching back to old year shows all historical data

### 5. Data Structure Example

**settings.json:**
```json
{
  "financialYear": "2026-2027",
  "compiledBy": "John Doe",
  ...
}
```

**budgets.json:**
```json
[
  {
    "financialYear": "2026-2027",
    "schoolName": "School A",
    "totalGrant": 5000000,
    "items": [...]
  },
  {
    "financialYear": "2027-2028",
    "schoolName": "School A",
    "totalGrant": 6000000,
    "items": [...]
  }
]
```

**credits.json:**
```json
[
  {
    "id": "credit_123",
    "financialYear": "2026-2027",
    "date": "2026-05-15",
    "lineItems": [...]
  },
  {
    "id": "credit_456",
    "financialYear": "2027-2028",
    "date": "2027-06-20",
    "lineItems": [...]
  }
]
```

### 6. Fresh Start for New Year

When selecting a new financial year that has no data:

**Budget Page:**
- Shows "Initialize Budget" button
- No budget items displayed
- Ready for new budget creation

**Credit Register:**
- Empty table
- "No credits recorded yet" message
- Ready for new credit entries

**Debit Register:**
- Empty table
- "No debits recorded yet" message
- Ready for new debit entries

**Grant Summary Dashboard:**
- All charts show zero
- All totals show K0
- Clean slate for new year

### 7. Accessing Historical Data

To view previous year data:
1. Go to Settings
2. Select the old financial year from dropdown
3. All pages immediately show that year's data
4. All reports, documents, and analytics reflect the selected year

## Benefits

✅ **Data Integrity**: Each year's data is completely separate
✅ **No Data Loss**: All historical data preserved permanently
✅ **Easy Switching**: One dropdown controls entire system
✅ **Clean Workflow**: New years start fresh and organized
✅ **Audit Trail**: Complete history available for any year
✅ **Compliance**: Meets accounting standards for year-end separation

## Technical Implementation

- **No URL Parameters**: Financial year not in URLs (cleaner, more secure)
- **Session-Independent**: Works across browser sessions
- **Persistent Storage**: Saved in settings.json file
- **Automatic Filtering**: All queries automatically use active year
- **Scalable**: Supports unlimited financial years

## User Experience

1. **First Time**: System defaults to 2026-2027
2. **Daily Use**: Users work in current year without thinking about it
3. **Year End**: Switch to new year in Settings, start fresh
4. **Reporting**: Switch back to any year to view historical data
5. **Auditing**: Access any year's complete records anytime
