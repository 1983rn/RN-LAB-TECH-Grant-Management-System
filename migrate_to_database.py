"""
Migrate from JSON files to multi-tenant database
This script moves all JSON data to the database with proper school_id isolation
"""
import json
import os
from database import get_db, hash_password

def migrate_json_to_database():
    """Migrate all JSON data to database"""
    
    # Get or create default school (NANJATI CDSS)
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Check if default school exists
        cursor.execute("SELECT id FROM schools WHERE username = ?", ('admin',))
        school = cursor.fetchone()
        
        if not school:
            # Create default school
            password_hash = hash_password('admin123')
            cursor.execute('''
                INSERT INTO schools (school_name, username, password_hash, is_active, subscription_status)
                VALUES (?, ?, ?, ?, ?)
            ''', ('NANJATI CDSS', 'admin', password_hash, 1, 'ACTIVE'))
            school_id = cursor.lastrowid
            print(f"✅ Created default school: NANJATI CDSS (ID: {school_id})")
        else:
            school_id = school['id']
            print(f"✅ Using existing school ID: {school_id}")
        
        # Migrate settings.json
        settings_file = 'data/settings.json'
        if os.path.exists(settings_file):
            with open(settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            
            financial_year = settings.get('financialYear', '2026-2027')
            total_grant = settings.get('totalGrantsByYear', {}).get(financial_year, 0)
            
            cursor.execute('''
                INSERT OR REPLACE INTO school_settings 
                (school_id, financial_year, school_address, ministry_department, total_grant,
                 compiled_by, entered_by, authorizing_officer, authorizing_appointment,
                 counter_sign, counter_appointment)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                school_id, financial_year,
                settings.get('schoolAddress', ''),
                settings.get('ministry', 'Education'),
                total_grant,
                settings.get('compiledBy', ''),
                settings.get('enteredBy', ''),
                settings.get('authorizingOfficer', ''),
                settings.get('authorizingAppointment', ''),
                settings.get('counterSign', ''),
                settings.get('counterAppointment', '')
            ))
            print(f"✅ Migrated settings for {financial_year}")
        
        # Migrate budgets.json
        budgets_file = 'data/budgets.json'
        if os.path.exists(budgets_file):
            with open(budgets_file, 'r', encoding='utf-8') as f:
                budgets = json.load(f)
            
            for budget in budgets:
                if isinstance(budget, dict):
                    financial_year = budget.get('financialYear', '2026-2027')
                    for item in budget.get('items', []):
                        cursor.execute('''
                            INSERT OR REPLACE INTO budget_items
                            (school_id, financial_year, item_key, pow_no, pow_name, sub_activity,
                             sub_item_description, code, total_allocation, monthly_allocations)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            school_id, financial_year, item.get('id'),
                            item.get('powNo'), item.get('powName'), item.get('subActivity'),
                            item.get('subItemDescription'), item.get('code'),
                            item.get('totalAllocation', 0),
                            json.dumps(item.get('monthlyAllocations', {}))
                        ))
            print(f"✅ Migrated budget items")
        
        # Migrate credits.json
        credits_file = 'data/credits.json'
        if os.path.exists(credits_file):
            with open(credits_file, 'r', encoding='utf-8') as f:
                credits = json.load(f)
            
            for credit in credits:
                if isinstance(credit, dict):
                    cursor.execute('''
                        INSERT INTO credits
                        (school_id, financial_year, date_received, month, line_items, remarks)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        school_id,
                        credit.get('financialYear', '2026-2027'),
                        credit.get('date'),
                        credit.get('month'),
                        json.dumps(credit.get('lineItems', [])),
                        credit.get('remarks', '')
                    ))
            print(f"✅ Migrated {len(credits)} credit entries")
        
        # Migrate debits.json
        debits_file = 'data/debits.json'
        if os.path.exists(debits_file):
            with open(debits_file, 'r', encoding='utf-8') as f:
                debits = json.load(f)
            
            for debit in debits:
                if isinstance(debit, dict):
                    cursor.execute('''
                        INSERT INTO debits
                        (school_id, financial_year, document_number, date_paid, month, item_id,
                         sub_item_description, code, description, amount, amount_words,
                         supplier_name, position, loose_minute_number, receipt_number)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        school_id,
                        debit.get('financialYear', '2026-2027'),
                        debit.get('documentNumber', ''),
                        debit.get('date'),
                        debit.get('month'),
                        debit.get('itemId'),
                        debit.get('subItemDescription'),
                        debit.get('code'),
                        debit.get('description'),
                        debit.get('amount', 0),
                        debit.get('amountWords', ''),
                        debit.get('supplierName', ''),
                        debit.get('position', ''),
                        debit.get('looseMinuteNumber', ''),
                        debit.get('receiptNumber', '')
                    ))
            print(f"✅ Migrated {len(debits)} debit entries")
        
        print("\n✅ Migration completed successfully!")
        print("⚠️  JSON files are still in place. You can back them up and delete them after verifying the migration.")

if __name__ == '__main__':
    migrate_json_to_database()
