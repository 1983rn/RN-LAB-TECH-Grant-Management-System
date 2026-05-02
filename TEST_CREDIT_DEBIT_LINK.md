# Test Credit-Debit Linking

## Quick Test Steps

1. **Login to the application**

2. **Go to Credit Register** and add a test credit:
   - Date: Today's date
   - Month: Current month
   - Select a budget item (e.g., "Wages for support staff")
   - Amount: K10,000
   - Click "Add Credit"

3. **Go to Debit Register** and click "Record Expenditure"
   - In the dropdown "Select Budget Sub-Item"
   - Find the same item you credited
   - It should show: "Wages for support staff (2211012204) - Bal: K10,000.00"

4. **If it shows K0.00 instead:**
   - Check that you're in the same financial year
   - Check that the credit was saved (go back to Credit Register)
   - Check browser console for JavaScript errors

## Debug Endpoint

Add this to app.py to test:

```python
@app.route('/debug/available_funds')
@require_login
def debug_available_funds():
    financial_year = get_financial_year()
    available = get_available_funds(financial_year)
    return jsonify({
        'financial_year': financial_year,
        'available_funds': {
            item_id: {
                'budgeted': funds['budgeted'],
                'credited': funds['credited'],
                'spent': funds['spent'],
                'balance': funds['balance']
            }
            for item_id, funds in available.items()
        }
    })
```

Then visit: `http://localhost:5176/debug/available_funds`

This will show you exactly what amounts are calculated for each budget item.
