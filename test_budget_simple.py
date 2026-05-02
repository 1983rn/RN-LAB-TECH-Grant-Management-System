#!/usr/bin/env python3
"""
Simple Budget Persistence Test - No Flask context required
"""
import sys
sys.path.insert(0, '.')

from db_helpers import get_school_budget, save_school_budget
from database import DATABASE_PATH
import sqlite3

def test_budget_simple():
    """Test budget persistence without Flask context"""
    print("=" * 60)
    print("SIMPLE BUDGET PERSISTENCE TEST")
    print("=" * 60)
    
    school_id = 5  # NANJATI CDSS
    financial_year = '2026-2027'
    
    print(f"\n1. School ID: {school_id}")
    print(f"   Financial Year: {financial_year}")
    print(f"   Database: {DATABASE_PATH}")
    
    # Step 1: Check current state
    print("\n2. Checking current budget state...")
    budget = get_school_budget(school_id, financial_year)
    
    if not budget:
        print("   No budget found - this is expected for fresh test")
        return False
    
    print(f"   Found {len(budget['items'])} budget items")
    
    # Step 2: Check if allocations are zero (indicating reset)
    zero_count = sum(1 for item in budget['items'] if item.get('totalAllocation', 0) == 0)
    non_zero_count = len(budget['items']) - zero_count
    
    print(f"   Items with zero allocation: {zero_count}")
    print(f"   Items with non-zero allocation: {non_zero_count}")
    
    if zero_count == len(budget['items']):
        print("   ⚠️ All items have zero allocation - possible reset issue")
    elif non_zero_count > 0:
        print("   ✅ Some items have allocations - data persists")
    
    # Step 3: Test save/load cycle
    print("\n3. Testing save/load cycle...")
    
    # Set test values
    test_values = [12345.67, 23456.78, 34567.89]
    for i in range(min(3, len(budget['items']))):
        budget['items'][i]['totalAllocation'] = test_values[i]
        print(f"   Setting item {i+1} to {test_values[i]}")
    
    # Save
    save_result = save_school_budget(school_id, financial_year, budget)
    print(f"   Save result: {save_result}")
    
    # Load again
    reloaded_budget = get_school_budget(school_id, financial_year)
    
    # Verify
    success = True
    for i in range(min(3, len(reloaded_budget['items']))):
        expected = test_values[i]
        actual = reloaded_budget['items'][i].get('totalAllocation', 0)
        if abs(actual - expected) < 0.01:
            print(f"   ✅ Item {i+1}: {actual} (correct)")
        else:
            print(f"   ❌ Item {i+1}: expected {expected}, got {actual}")
            success = False
    
    # Step 4: Check database directly
    print("\n4. Direct database verification...")
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT COUNT(*) FROM budget_items 
        WHERE school_id = ? AND financial_year = ? AND total_allocation > 0
    ''', (school_id, financial_year))
    positive_count = cursor.fetchone()[0]
    
    cursor.execute('''
        SELECT COUNT(*) FROM budget_items 
        WHERE school_id = ? AND financial_year = ?
    ''', (school_id, financial_year))
    total_count = cursor.fetchone()[0]
    
    print(f"   Total budget items: {total_count}")
    print(f"   Items with positive allocation: {positive_count}")
    
    conn.close()
    
    # Step 5: Summary
    print("\n" + "=" * 60)
    if success and positive_count > 0:
        print("✅ SUCCESS: Budget persistence working!")
        print("   - Data saves correctly")
        print("   - Data loads correctly") 
        print("   - Database contains saved values")
    else:
        print("❌ ISSUES DETECTED:")
        if not success:
            print("   - Save/load cycle failed")
        if positive_count == 0:
            print("   - No positive allocations in database")
            print("   - Possible reset/overwrite issue")
    
    print("=" * 60)
    return success and positive_count > 0

if __name__ == '__main__':
    test_budget_simple()
