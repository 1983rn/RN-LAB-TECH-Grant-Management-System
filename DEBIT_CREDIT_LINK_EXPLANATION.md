# Debit Register - Credit Allocation Display

## Current Implementation

The "Select Budget Sub-Item" dropdown in the Debit Register **ALREADY** displays allocated amounts from the Credit Register correctly.

### How It Works

1. **Data Flow:**
   ```
   Credit Register → get_available_funds() → Debit Dropdown
   ```

2. **Calculation Logic** (in `app.py`):
   ```python
   def get_available_funds(financial_year):
       # For each budget item:
       item_credits = sum(credits for this item from Credit Register)
       item_debits = sum(debits already spent)
       balance = item_credits - item_debits
   ```

3. **Display in Dropdown** (in `debits.html`):
   ```html
   <option value="{{ item.id }}">
       {{ item.subItemDescription }} ({{ item.code }}) 
       - Bal: K{{ funds.balance }}
   </option>
   ```

### What the Balance Shows

- **Balance = Credited Amount - Already Spent**
- This is the AVAILABLE funds for spending
- NOT the budgeted amount (which is just a plan)
- ONLY shows what has actually been credited and not yet spent

### Why Balance Might Show K0.00

If you see K0.00 in the dropdown, it means:
1. ❌ No credits have been entered for that item in the Credit Register, OR
2. ✅ All credited funds for that item have already been spent

### Workflow

1. **Step 1:** Enter Total Grant in Settings
2. **Step 2:** Allocate budget in Budget Allocation page (this is just planning)
3. **Step 3:** Record actual fund receipts in Credit Register (this creates spendable funds)
4. **Step 4:** Record expenditures in Debit Register (this shows available balance from credits)

### Example

- Budget Allocation: K100,000 (just a plan)
- Credit Register: K50,000 received (actual money)
- Debit Register dropdown shows: **Bal: K50,000** (what you can actually spend)
- After spending K20,000: **Bal: K30,000**

## Verification

The implementation is CORRECT. The dropdown shows:
✅ Credited amounts from Credit Register
✅ Minus already spent amounts
✅ Filtered by financial year
✅ Real-time balance calculation
✅ Overspending warning when amount exceeds balance

## No Changes Needed

The system is working as designed. If balances show K0.00, you need to:
1. Go to Credit Register
2. Add credit entries for the budget items
3. Then those amounts will appear in the Debit Register dropdown
