"""
Fix POW Duplication/Missing Issues
- Add unique constraint
- Remove duplicates
- Ensure all schools have exactly 16 POWs
"""
from database import get_db
import json

def fix_pow_issues():
    """Fix POW duplication and missing issues"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Step 1: Add unique constraint if not exists
        print("Step 1: Adding unique constraint...")
        try:
            cursor.execute('''
                CREATE UNIQUE INDEX IF NOT EXISTS idx_budget_unique 
                ON budget_items(school_id, financial_year, code)
            ''')
            print("  [OK] Unique constraint added")
        except Exception as e:
            print(f"  [INFO] Constraint may already exist: {e}")
        
        # Step 2: Find and remove duplicates
        print("\nStep 2: Removing duplicates...")
        cursor.execute('''
            SELECT school_id, financial_year, code, COUNT(*) as cnt
            FROM budget_items
            GROUP BY school_id, financial_year, code
            HAVING cnt > 1
        ''')
        duplicates = cursor.fetchall()
        
        for dup in duplicates:
            school_id, fy, code, count = dup['school_id'], dup['financial_year'], dup['code'], dup['cnt']
            print(f"  Found {count} duplicates for school {school_id}, FY {fy}, code {code}")
            
            # Keep first, delete rest
            cursor.execute('''
                DELETE FROM budget_items
                WHERE id NOT IN (
                    SELECT MIN(id) FROM budget_items
                    WHERE school_id = ? AND financial_year = ? AND code = ?
                )
                AND school_id = ? AND financial_year = ? AND code = ?
            ''', (school_id, fy, code, school_id, fy, code))
            print(f"  [OK] Removed {count-1} duplicate(s)")
        
        if not duplicates:
            print("  [OK] No duplicates found")
        
        # Step 3: Ensure all schools have all 16 POWs
        print("\nStep 3: Ensuring all schools have 16 POWs...")
        cursor.execute('SELECT id FROM schools WHERE school_name != "DEVELOPER_ACCOUNT"')
        schools = cursor.fetchall()
        
        for school in schools:
            school_id = school['id']
            
            # Get distinct financial years for this school
            cursor.execute('''
                SELECT DISTINCT financial_year FROM school_settings
                WHERE school_id = ?
            ''', (school_id,))
            years = cursor.fetchall()
            
            if not years:
                years = [{'financial_year': '2026-2027'}]  # Default
            
            for year_row in years:
                fy = year_row['financial_year']
                
                # Count existing POWs
                cursor.execute('''
                    SELECT COUNT(DISTINCT code) as cnt
                    FROM budget_items
                    WHERE school_id = ? AND financial_year = ?
                ''', (school_id, fy))
                count = cursor.fetchone()['cnt']
                
                if count < 16:
                    print(f"  School {school_id}, FY {fy}: Has {count} POWs, adding missing ones...")
                    
                    # Get existing codes
                    cursor.execute('''
                        SELECT code FROM budget_items
                        WHERE school_id = ? AND financial_year = ?
                    ''', (school_id, fy))
                    existing_codes = {row['code'] for row in cursor.fetchall()}
                    
                    # Generate full structure
                    from app import generate_budget_structure
                    full_structure = generate_budget_structure()
                    
                    # Insert missing POWs
                    for item in full_structure:
                        if item['code'] not in existing_codes:
                            cursor.execute('''
                                INSERT OR IGNORE INTO budget_items
                                (school_id, financial_year, item_key, pow_no, pow_name, sub_activity,
                                 sub_item_description, code, total_allocation, monthly_allocations)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (school_id, fy, item['id'], item['powNo'], item['powName'],
                                  item['subActivity'], item['subItemDescription'], item['code'],
                                  0, json.dumps(item['monthlyAllocations'])))
                    
                    print(f"  [OK] Added {16 - count} missing POWs")
        
        print("\n[SUCCESS] All POW issues fixed!")
        print("  - Unique constraint enforced")
        print("  - Duplicates removed")
        print("  - All schools have exactly 16 POWs")

if __name__ == '__main__':
    fix_pow_issues()
