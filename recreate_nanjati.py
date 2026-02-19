"""
Recreate NANJATI CDSS school with proper template
"""
import sqlite3
import json
import hashlib
from datetime import datetime, timedelta

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def recreate_nanjati():
    conn = sqlite3.connect('data/grant_management.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Check if NANJATI exists
    cursor.execute("SELECT id FROM schools WHERE username = 'NANJATICDSS'")
    existing = cursor.fetchone()
    
    if existing:
        print(f"NANJATI CDSS already exists with ID {existing['id']}")
        school_id = existing['id']
    else:
        # Create NANJATI CDSS
        password_hash = hash_password('1994')
        trial_start = datetime.now()
        trial_end = trial_start + timedelta(days=30)
        
        cursor.execute('''INSERT INTO schools 
            (school_name, username, password_hash, is_active, subscription_status, 
             subscription_start, subscription_end) 
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            ('NANJATI CDSS', 'NANJATICDSS', password_hash, 1, 'TRIAL', 
             trial_start.strftime('%Y-%m-%d'), trial_end.strftime('%Y-%m-%d')))
        school_id = cursor.lastrowid
        print(f"Created NANJATI CDSS with ID {school_id}")
    
    # Initialize settings
    financial_year = '2026-2027'
    cursor.execute('''INSERT OR REPLACE INTO school_settings
        (school_id, financial_year, school_name, total_grant)
        VALUES (?, ?, ?, ?)''',
        (school_id, financial_year, 'NANJATI CDSS', 0))
    print(f"Initialized settings for FY {financial_year}")
    
    # Delete existing budget items
    cursor.execute('DELETE FROM budget_items WHERE school_id = ?', (school_id,))
    print(f"Cleared old budget items")
    
    # Import master template
    import sys
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    from app import generate_budget_structure
    
    master_template = generate_budget_structure()
    
    # Insert all 42 rows
    for item in master_template:
        cursor.execute('''INSERT INTO budget_items
            (school_id, financial_year, template_row_id, item_key, pow_no, pow_name,
             sub_activity, sub_item_description, code, total_allocation, monthly_allocations)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (school_id, financial_year, item['template_row_id'], item['id'],
             item['powNo'], item['powName'], item['subActivity'],
             item['subItemDescription'], item['code'], 0,
             json.dumps(item['monthlyAllocations'])))
    
    conn.commit()
    conn.close()
    
    print(f"\n[SUCCESS] NANJATI CDSS ready!")
    print(f"  - School ID: {school_id}")
    print(f"  - Username: NANJATICDSS")
    print(f"  - Password: 1994")
    print(f"  - Budget rows: {len(master_template)}")

if __name__ == '__main__':
    recreate_nanjati()
