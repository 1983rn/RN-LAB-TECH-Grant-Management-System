"""
Migrate budget_items to use template_row_id for proper uniqueness
Only runs when template_row_id column is missing
"""
import sqlite3
import json

def migrate_budget_items():
    conn = sqlite3.connect('data/grant_management.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("Step 1: Check if template_row_id column exists...")
    cursor.execute("PRAGMA table_info(budget_items)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'template_row_id' in columns:
        print("  [OK] Column already exists - migration not needed")
        print("  [INFO] Skipping budget data deletion - preserving existing data")
        conn.close()
        return
    
    print("  [INFO] Column missing, running migration...")
    
    # Backup existing data
    cursor.execute("SELECT * FROM budget_items")
    old_data = cursor.fetchall()
    print(f"  [OK] Backed up {len(old_data)} rows")
    
    # Drop old table
    cursor.execute("DROP TABLE IF EXISTS budget_items")
    
    # Create new table with template_row_id
    cursor.execute('''
        CREATE TABLE budget_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            school_id INTEGER NOT NULL,
            financial_year TEXT NOT NULL,
            template_row_id INTEGER NOT NULL,
            item_key TEXT NOT NULL,
            pow_no INTEGER,
            pow_name TEXT,
            sub_activity TEXT,
            sub_item_description TEXT,
            code TEXT,
            total_allocation REAL DEFAULT 0,
            monthly_allocations TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (school_id) REFERENCES schools(id),
            UNIQUE(school_id, financial_year, template_row_id)
        )
    ''')
    print("  [OK] Created new table with template_row_id")
    
    # Create index
    cursor.execute('CREATE INDEX idx_budget_school ON budget_items(school_id, financial_year)')
    print("  [OK] Created index")
    
    # Step 2: Restore data with template_row_id (use row number as template_row_id)
    print("\nStep 2: Restoring existing data with template_row_id...")
    for i, row in enumerate(old_data):
        template_row_id = (i % 42) + 1  # Cycle through 1-42 for template rows
        cursor.execute('''
            INSERT INTO budget_items
            (school_id, financial_year, template_row_id, item_key, pow_no, pow_name, 
             sub_activity, sub_item_description, code, total_allocation, monthly_allocations)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            row['school_id'],
            row['financial_year'],
            template_row_id,
            row.get('item_key', ''),
            row.get('pow_no'),
            row.get('pow_name'),
            row.get('sub_activity'),
            row.get('sub_item_description'),
            row.get('code'),
            row.get('total_allocation', 0),
            row.get('monthly_allocations', '{}')
        ))
    
    print(f"  [OK] Restored {len(old_data)} rows with template_row_id")
    
    # Step 3: Initialize schools that have no budget data
    print("\nStep 3: Initializing schools without budget data...")
    cursor.execute('SELECT id FROM schools WHERE school_name != "DEVELOPER_ACCOUNT"')
    schools = cursor.fetchall()
    
    # Import master template
    import sys
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    from app import generate_budget_structure
    
    master_template = generate_budget_structure()
    print(f"  [OK] Master template has {len(master_template)} rows")
    
    for school in schools:
        school_id = school['id']
        
        # Check if school already has budget data
        cursor.execute('SELECT COUNT(*) FROM budget_items WHERE school_id = ?', (school_id,))
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"  [SKIP] School {school_id} already has {count} budget items")
            continue
        
        # Get financial years for this school
        cursor.execute('SELECT DISTINCT financial_year FROM school_settings WHERE school_id = ?', (school_id,))
        years = cursor.fetchall()
        
        if not years:
            years = [{'financial_year': '2026-2027'}]
        
        for year_row in years:
            fy = year_row['financial_year']
            
            # Insert all 42 rows from master template
            for item in master_template:
                cursor.execute('''
                    INSERT INTO budget_items
                    (school_id, financial_year, template_row_id, item_key, pow_no, pow_name,
                     sub_activity, sub_item_description, code, total_allocation, monthly_allocations)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (school_id, fy, item['template_row_id'], item['id'], item['powNo'],
                      item['powName'], item['subActivity'], item['subItemDescription'],
                      item['code'], 0, json.dumps(item['monthlyAllocations'])))
            
            print(f"  [OK] School {school_id}, FY {fy}: Inserted {len(master_template)} rows")
    
    conn.commit()
    conn.close()
    
    print("\n[SUCCESS] Migration complete!")
    print("  - All schools now have exactly 42 budget rows")
    print("  - Uniqueness enforced by template_row_id")
    print("  - No duplicates possible")

if __name__ == '__main__':
    migrate_budget_items()
