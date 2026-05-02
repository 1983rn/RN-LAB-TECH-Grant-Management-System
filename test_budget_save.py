"""Test budget save functionality"""
import sys
sys.path.insert(0, '.')

from db_helpers import get_school_budget, save_school_budget

# Test with NANJATI CDSS (school_id=5)
school_id = 5
financial_year = '2026-2027'

print("Step 1: Get current budget...")
budget = get_school_budget(school_id, financial_year)
print(f"  Found {len(budget['items'])} items")
print(f"  First item has template_row_id: {budget['items'][0].get('template_row_id')}")

print("\nStep 2: Modify first item allocation...")
budget['items'][0]['totalAllocation'] = 1000.0
budget['items'][0]['monthlyAllocations']['April'] = 100.0

print("\nStep 3: Save budget...")
result = save_school_budget(school_id, financial_year, budget)
print(f"  Save result: {result}")

print("\nStep 4: Verify save...")
budget2 = get_school_budget(school_id, financial_year)
print(f"  First item allocation: {budget2['items'][0]['totalAllocation']}")
print(f"  April allocation: {budget2['items'][0]['monthlyAllocations']['April']}")

if budget2['items'][0]['totalAllocation'] == 1000.0:
    print("\n[SUCCESS] Budget save works correctly!")
else:
    print("\n[ERROR] Budget save failed!")
