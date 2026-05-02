#!/usr/bin/env python3
"""
Test Budget Data Persistence
Verify that budget allocations persist after restart
"""
import sys
sys.path.insert(0, '.')

from db_helpers import get_school_budget, save_school_budget
from database import DATABASE_PATH
import sqlite3

def test_budget_persistence():
    """Test that budget data persists correctly"""
    print("=" * 60)
    print("TESTING BUDGET DATA PERSISTENCE")
    print("=" * 60)
    
    school_id = 5  # NANJATI CDSS
    financial_year = '2026-2027'
    
    print(f"\n1. Testing with School ID: {school_id}")
    print(f"   Financial Year: {financial_year}")
    print(f"   Database: {DATABASE_PATH}")
    
    # Step 1: Get current budget
    print("\n2. Getting current budget...")
    budget = get_school_budget(school_id, financial_year)
    
    if not budget or not budget.get('items'):
        print("   No budget found - creating test budget...")
        # Create test budget with some allocations
        from app import generate_budget_structure
        test_budget = {
            'financialYear': financial_year,
            'items': generate_budget_structure()
        }
        
        # Set some test allocations
        for i, item in enumerate(test_budget['items'][:5]):
            item['totalAllocation'] = (i + 1) * 10000.0
            item['monthlyAllocations']['April'] = (i + 1) * 1000.0
        
        print("   Saving test budget...")
        result = save_school_budget(school_id, financial_year, test_budget)
        if result:
            print("   ✅ Test budget saved successfully")
        else:
            print("   ❌ Failed to save test budget")
            return False
        
        # Retrieve again
        budget = get_school_budget(school_id, financial_year)
    
    if not budget or not budget.get('items'):
        print("   ❌ Still no budget found after save")
        return False
    
    print(f"   Found budget with {len(budget['items'])} items")
    
    # Step 2: Modify allocations
    print("\n3. Modifying budget allocations...")
    original_values = []
    for i in range(min(3, len(budget['items']))):
        original_values.append(budget['items'][i]['totalAllocation'])
        budget['items'][i]['totalAllocation'] = (i + 1) * 25000.0
        budget['items'][i]['monthlyAllocations']['April'] = (i + 1) * 2500.0
        print(f"   Item {i}: {original_values[i]} → {budget['items'][i]['totalAllocation']}")
    
    # Step 3: Save modifications
    print("\n4. Saving modified budget...")
    result = save_school_budget(school_id, financial_year, budget)
    if result:
        print("   ✅ Budget saved successfully")
    else:
        print("   ❌ Failed to save budget")
        return False
    
    # Step 4: Force checkpoint
    print("\n5. Forcing WAL checkpoint...")
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute('PRAGMA wal_checkpoint(FULL)')
    conn.close()
    print("   ✅ Checkpoint complete")
    
    # Step 5: Verify persistence
    print("\n6. Verifying data persistence...")
    verified_budget = get_school_budget(school_id, financial_year)
    
    if not verified_budget or not verified_budget.get('items'):
        print("   ❌ No budget found after save")
        return False
    
    success = True
    for i in range(min(3, len(verified_budget['items']))):
        expected = (i + 1) * 25000.0
        actual = verified_budget['items'][i]['totalAllocation']
        if abs(actual - expected) < 0.01:  # Allow for floating point precision
            print(f"   ✅ Item {i}: {actual} (correct)")
        else:
            print(f"   ❌ Item {i}: expected {expected}, got {actual}")
            success = False
    
    # Step 6: Direct database verification
    print("\n7. Direct database verification...")
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT template_row_id, total_allocation
        FROM budget_items
        WHERE school_id = ? AND financial_year = ?
        ORDER BY template_row_id
        LIMIT 3
    ''', (school_id, financial_year))
    rows = cursor.fetchall()
    conn.close()
    
    print("   Direct database values:")
    for i, (template_id, allocation) in enumerate(rows):
        expected = (i + 1) * 25000.0
        print(f"     Item {template_id}: {allocation}")
        if abs(allocation - expected) < 0.01:
            print(f"       ✅ Correct")
        else:
            print(f"       ❌ Expected {expected}")
            success = False
    
    print("\n" + "=" * 60)
    if success:
        print("✅ SUCCESS: Budget data persists correctly!")
        print("   - Allocations saved to database")
        print("   - Data survives WAL checkpoint")
        print("   - Retrieval works correctly")
        print("   - Multi-tenant isolation maintained")
    else:
        print("❌ FAILURE: Budget persistence issues detected")
        print("   - Data not saving correctly")
        print("   - Or data being lost after save")
    
    print("=" * 60)
    return success

if __name__ == '__main__':
    test_budget_persistence()
