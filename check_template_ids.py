"""Check if budget items have template_row_id in frontend"""
import sys
sys.path.insert(0, '.')

from db_helpers import get_school_budget

school_id = 5  # NANJATI CDSS
financial_year = '2026-2027'

budget = get_school_budget(school_id, financial_year)

print(f"Total items: {len(budget['items'])}")
print("\nFirst 3 items:")
for i, item in enumerate(budget['items'][:3]):
    print(f"\nItem {i+1}:")
    print(f"  id: {item.get('id')}")
    print(f"  template_row_id: {item.get('template_row_id')}")
    print(f"  powNo: {item.get('powNo')}")
    print(f"  code: {item.get('code')}")

# Check if all items have template_row_id
missing = [i for i, item in enumerate(budget['items']) if not item.get('template_row_id')]
if missing:
    print(f"\n[ERROR] {len(missing)} items missing template_row_id: {missing}")
else:
    print(f"\n[OK] All {len(budget['items'])} items have template_row_id")
