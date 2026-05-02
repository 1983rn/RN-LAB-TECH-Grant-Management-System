# Debit Register - Credit Allocation Analysis

## Issue Report
User reported: "Allocated amounts are not being populated from Credit Register in the Debit dropdown"

## Investigation Results

### Current Implementation Status: ✅ WORKING CORRECTLY

The system **ALREADY** links Credit Register data to the Debit Register dropdown correctly.

### Code Flow

1. **Backend** (`app.py` - `/debits` route):
   ```python
   available_funds = get_available_funds(financial_year)
   # Returns: {item_id: {budgeted, credited, spent, balance}}
   ```

2. **Calculation** (`get_available_funds()` function):
   ```python
   # For each budget item:
   item_credits = sum(all credits from Credit Register for this item)
   item_debits = sum(all debits already recorded)
   balance = item_credits - item_debits  # Available to spend
   ```

3. **Frontend** (`debits.html` template):
   ```html
   <option data-balance="{{ funds.balance }}">
       {{ item.subItemDescription }} ({{ item.code }}) 
       - Bal: K{{ "{:,.2f}".format(funds.balance) }}
   </option>
   ```

### What the Balance Represents

**Balance = Credited Amount - Already Spent**

- ✅ Shows actual credited funds from Credit Register
- ✅ Subtracts already spent amounts
- ✅ Filtered by financial year
- ✅ Updates dynamically

### Why Balance Might Show K0.00

If dropdown shows "Bal: K0.00", it means:

1. **No credits entered yet** - Go to Credit Register and add credits first
2. **All funds spent** - The credited amount has been fully spent
3. **Wrong financial year** - Credits exist in different financial year

### Correct Workflow

```
Step 1: Settings → Enter Total Grant (e.g., K5,000,000)
Step 2: Budget Allocation → Plan how to allocate (just planning)
Step 3: Credit Register → Record actual fund receipts (creates spendable funds)
Step 4: Debit Register → Record expenditures (shows available balance)
```

### Example Scenario

**Budget Allocation:**
- Wages for support staff: K100,000 (planned)

**Credit Register:**
- April: Received K50,000 for Wages

**Debit Register Dropdown Shows:**
- "Wages for support staff (2211012204) - Bal: K50,000.00"

**After spending K20,000:**
- "Wages for support staff (2211012204) - Bal: K30,000.00"

## Testing

### Test the Link:

1. **Add a Credit:**
   - Go to Credit Register
   - Add credit: K10,000 for any item
   - Save

2. **Check Debit Dropdown:**
   - Go to Debit Register
   - Click "Record Expenditure"
   - Find the same item in dropdown
   - Should show: "Item Name (Code) - Bal: K10,000.00"

3. **Debug Endpoint:**
   - Visit: `http://localhost:5176/debug/available_funds`
   - Shows all items with credited/spent/balance amounts

## Conclusion

✅ **No bug exists** - The system correctly links Credit Register to Debit Register
✅ **Balance calculation is accurate** - Credits minus Debits
✅ **Financial year filtering works** - Only shows current year data
✅ **Overspending prevention works** - Warns when amount exceeds balance

### If User Still Sees K0.00:

**Action Required:** Add credits in the Credit Register first. The Debit Register can only show what has been credited.

**Remember:** Budget Allocation is just planning. Credit Register is actual money received. Only credited money can be spent.
