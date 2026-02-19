"""
Migration script to convert single-tenant to multi-tenant
"""
import json
import os
from database import init_database, get_db, hash_password
from datetime import datetime, timedelta

def migrate_existing_data():
    """Migrate existing JSON data to multi-tenant database"""
    
    print("🔄 Starting migration to multi-tenant architecture...")
    
    # Initialize new database
    init_database()
    
    # Check if old data exists
    old_data_dir = 'data'
    budgets_file = os.path.join(old_data_dir, 'budgets.json')
    credits_file = os.path.join(old_data_dir, 'credits.json')
    debits_file = os.path.join(old_data_dir, 'debits.json')
    settings_file = os.path.join(old_data_dir, 'settings.json')
    
    if not os.path.exists(budgets_file):
        print("ℹ️  No existing data found. Starting fresh.")
        return
    
    # Create default school from existing data
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Load old settings to get school name
        school_name = "NANJATI CDSS"  # Default
        if os.path.exists(settings_file):
            with open(settings_file, 'r') as f:
                old_settings = json.load(f)
                if isinstance(old_settings, dict):
                    school_name = old_settings.get('ministry', 'NANJATI CDSS')
        
        # Create default school account
        default_username = "admin"
        default_password = "admin123"
        password_hash = hash_password(default_password)
        
        cursor.execute('''
            INSERT INTO schools (school_name, username, password_hash, is_active, 
                               subscription_status, subscription_end)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (school_name, default_username, password_hash, 1, 'PAID', 
              (datetime.now() + timedelta(days=365)).date()))
        
        school_id = cursor.lastrowid
        print(f"✅ Created default school: {school_name}")
        print(f"   Username: {default_username}")
        print(f"   Password: {default_password}")
        
        # Migrate budgets
        if os.path.exists(budgets_file):
            with open(budgets_file, 'r') as f:
                budgets = json.load(f)
                for budget in budgets:
                    if isinstance(budget, dict):
                        financial_year = budget.get('financialYear', '2026-2027')
                        
                        # Migrate settings
                        cursor.execute('''
                            INSERT OR REPLACE INTO school_settings 
                            (school_id, financial_year, school_address, total_grant)
                            VALUES (?, ?, ?, ?)
                        ''', (school_id, financial_year, '', budget.get('totalGrant', 0)))
                        
                        # Migrate budget items
                        for item in budget.get('items', []):
                            cursor.execute('''
                                INSERT INTO budget_items 
                                (school_id, financial_year, item_key, pow_no, pow_name, 
                                 sub_activity, sub_item_description, code, total_allocation, 
                                 monthly_allocations)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (school_id, financial_year, item.get('id'), 
                                  item.get('powNo'), item.get('powName'),
                                  item.get('subActivity'), item.get('subItemDescription'),
                                  item.get('code'), item.get('totalAllocation', 0),
                                  json.dumps(item.get('monthlyAllocations', {}))))
            print("✅ Migrated budget data")
        
        # Migrate credits
        if os.path.exists(credits_file):
            with open(credits_file, 'r') as f:
                credits = json.load(f)
                for credit in credits:
                    if isinstance(credit, dict):
                        cursor.execute('''
                            INSERT INTO credits 
                            (school_id, financial_year, date_received, month, line_items, remarks)
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', (school_id, credit.get('financialYear', '2026-2027'),
                              credit.get('date'), credit.get('month'),
                              json.dumps(credit.get('lineItems', [])),
                              credit.get('remarks', '')))
            print("✅ Migrated credit data")
        
        # Migrate debits
        if os.path.exists(debits_file):
            with open(debits_file, 'r') as f:
                debits = json.load(f)
                for debit in debits:
                    if isinstance(debit, dict):
                        cursor.execute('''
                            INSERT INTO debits 
                            (school_id, financial_year, document_number, date_paid, month,
                             item_id, sub_item_description, code, description, amount,
                             amount_words, supplier_name, position, loose_minute_number,
                             receipt_number)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (school_id, debit.get('financialYear', '2026-2027'),
                              debit.get('documentNumber', '0001'), debit.get('date'),
                              debit.get('month'), debit.get('itemId'),
                              debit.get('subItemDescription'), debit.get('code'),
                              debit.get('description'), debit.get('amount', 0),
                              debit.get('amountWords', ''), debit.get('supplierName'),
                              debit.get('position'), debit.get('looseMinuteNumber'),
                              debit.get('receiptNumber')))
            print("✅ Migrated debit data")
        
        # Migrate settings
        if os.path.exists(settings_file):
            with open(settings_file, 'r') as f:
                settings = json.load(f)
                if isinstance(settings, dict):
                    financial_year = settings.get('financialYear', '2026-2027')
                    cursor.execute('''
                        INSERT OR REPLACE INTO school_settings 
                        (school_id, financial_year, school_address, ministry_department,
                         total_grant, compiled_by, entered_by, authorizing_officer,
                         authorizing_appointment, counter_sign, counter_appointment)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (school_id, financial_year, settings.get('schoolAddress', ''),
                          settings.get('ministry', 'Education'),
                          settings.get('totalGrantsByYear', {}).get(financial_year, 0),
                          settings.get('compiledBy', ''), settings.get('enteredBy', ''),
                          settings.get('authorizingOfficer', ''),
                          settings.get('authorizingAppointment', ''),
                          settings.get('counterSign', ''),
                          settings.get('counterAppointment', '')))
            print("✅ Migrated settings data")
    
    print("\n✅ Migration completed successfully!")
    print(f"\n📝 Default School Credentials:")
    print(f"   School: {school_name}")
    print(f"   Username: {default_username}")
    print(f"   Password: {default_password}")
    print(f"\n🔐 Developer Credentials:")
    print(f"   Username: juniornsambe@yahoo.com")
    print(f"   Password: blessings19831983/")
    print(f"   Access: Type 'devaccess' on login screen")

if __name__ == '__main__':
    migrate_existing_data()
