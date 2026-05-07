import sqlite3
import json
import os
from datetime import datetime

# Multi-Tenant Restoration Script (Fix: Added Template Row ID matching)
# This script restores data from JSON backups while maintaining strict school isolation.

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data', 'grant_management.db')
BUDGETS_JSON = os.path.join(BASE_DIR, 'data', 'budgets.json')
CREDITS_JSON = os.path.join(BASE_DIR, 'data', 'credits.json')
DEBITS_JSON = os.path.join(BASE_DIR, 'data', 'debits.json')
SETTINGS_JSON = os.path.join(BASE_DIR, 'data', 'settings.json')

# Master Template mapping for deriving missing template_row_ids
MASTER_TEMPLATE = [
    {'tid': 1, 'pow': '1', 'desc': 'Wages for support staff', 'code': '2211012204'},
    {'tid': 2, 'pow': '1', 'desc': 'Public transport', 'code': '2211011203'},
    {'tid': 3, 'pow': '1', 'desc': 'Heating and lighting', 'code': '2211011401'},
    {'tid': 4, 'pow': '1', 'desc': 'Telephone charges', 'code': '2211011402'},
    {'tid': 5, 'pow': '1', 'desc': 'Water and sanitation', 'code': '2211011405'},
    {'tid': 6, 'pow': '1', 'desc': 'Consumable stores', 'code': '2211011502'},
    {'tid': 7, 'pow': '1', 'desc': 'Postage', 'code': '2211011504'},
    {'tid': 8, 'pow': '1', 'desc': 'Printing cost', 'code': '2211011505'},
    {'tid': 9, 'pow': '1', 'desc': 'Publication and advertisement', 'code': '2211011406'},
    {'tid': 10, 'pow': '1', 'desc': 'Stationery', 'code': '2211011506'},
    {'tid': 11, 'pow': '1', 'desc': 'Uniform and protective wear', 'code': '2211011507'},
    {'tid': 12, 'pow': '1', 'desc': 'Fuel and Lubricants', 'code': '2211012401'},
    {'tid': 13, 'pow': '1', 'desc': 'Subscriptions', 'code': '2211012321'},
    {'tid': 14, 'pow': '1', 'desc': 'Purchase of plant and office equipment', 'code': '2211010251'},
    {'tid': 15, 'pow': '2', 'desc': 'Examinations', 'code': '2211011803'},
    {'tid': 16, 'pow': '3', 'desc': 'Fuel 0r 2103 public transport', 'code': '2211012401'},
    {'tid': 17, 'pow': '3', 'desc': 'Subsistence allowance', 'code': '2211011204'},
    {'tid': 18, 'pow': '4', 'desc': 'Fuel or 2103 public transport', 'code': '2211012401'},
    {'tid': 19, 'pow': '4', 'desc': 'Subsistence allowance', 'code': '2211011204'},
    {'tid': 20, 'pow': '5', 'desc': 'Sporting equipment', 'code': '2211011805'},
    {'tid': 21, 'pow': '5', 'desc': 'Fuel or 1203-Public transport', 'code': '2211012401'},
    {'tid': 22, 'pow': '5', 'desc': 'Subsistence allowance', 'code': '2211011204'},
    {'tid': 23, 'pow': '6', 'desc': 'Purchase of special needs materials', 'code': '2211011806'},
    {'tid': 24, 'pow': '7', 'desc': 'Science consumables', 'code': '2211011807'},
    {'tid': 25, 'pow': '7', 'desc': 'Text books', 'code': '2211011804'},
    {'tid': 26, 'pow': '7', 'desc': 'Purchase of school supplies', 'code': '2211011808'},
    {'tid': 27, 'pow': '8', 'desc': 'HIV/AIDS services', 'code': '2211011614'},
    {'tid': 28, 'pow': '8', 'desc': 'Drugs', 'code': '2211011601'},
    {'tid': 29, 'pow': '9', 'desc': 'Maintenance of buildings', 'code': '2211012501'},
    {'tid': 30, 'pow': '9', 'desc': 'Maintenance of water supplies', 'code': '2211012504'},
    {'tid': 31, 'pow': '10', 'desc': 'Subscription', 'code': '2211012321'},
    {'tid': 32, 'pow': '10', 'desc': 'Subscription', 'code': '2211012321'},
    {'tid': 33, 'pow': '11', 'desc': 'Consumables', 'code': '2211011502'},
    {'tid': 34, 'pow': '11', 'desc': 'Subsistence Allowances', 'code': '2211011204'},
    {'tid': 35, 'pow': '11', 'desc': 'Public transport or 2401 fuel', 'code': '2211011203'},
    {'tid': 36, 'pow': '12', 'desc': 'Subsistence Allowances', 'code': '2211011204'},
    {'tid': 37, 'pow': '12', 'desc': 'Public transport or 2401 fuel', 'code': '2211011203'},
    {'tid': 38, 'pow': '13', 'desc': 'Consumables', 'code': '2211011502'},
    {'tid': 39, 'pow': '14', 'desc': 'Consumables', 'code': '2211011502'},
    {'tid': 40, 'pow': '15', 'desc': 'Boarding expenses', 'code': '2211011801'},
    {'tid': 41, 'pow': '16', 'desc': 'Subsistence Allowances', 'code': '2211011204'},
    {'tid': 42, 'pow': '16', 'desc': 'Public transport or 2401 fuel', 'code': '2211011203'},
]

def find_template_id(pow_no, desc, code):
    # Try exact match
    for row in MASTER_TEMPLATE:
        if str(row['pow']) == str(pow_no) and row['desc'] == desc and row['code'] == code:
            return row['tid']
    # Try fuzzy match (desc and code)
    for row in MASTER_TEMPLATE:
        if row['desc'] == desc and row['code'] == code:
            return row['tid']
    return None

def restore_data():
    print("🚀 Starting Multi-Tenant Data Restoration...")
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Error: Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    target_year = "2026-2027"
    target_term = "Term 3"
    legacy_fy = f"{target_year}_{target_term}"

    # 1. Map School Names to Database IDs
    cursor.execute("SELECT id, school_name FROM schools")
    db_schools = cursor.fetchall()
    name_to_id = {row['school_name'].upper(): row['id'] for row in db_schools}
    
    nanjati_id = None
    for name, sid in name_to_id.items():
        if "NANJATI" in name:
            nanjati_id = sid
            print(f"✅ Identified Nanjati CDSS in database (ID: {sid})")
            break
    
    if not nanjati_id:
        cursor.execute("SELECT id, school_name FROM schools WHERE username = 'admin'")
        admin_school = cursor.fetchone()
        if admin_school:
            nanjati_id = admin_school['id']
            print(f"✅ Using default admin school (ID: {nanjati_id}) as Nanjati target.")
        else:
            print("❌ Error: Could not find a suitable target school ID.")
            conn.close()
            return

    # 2. Update Term Settings
    cursor.execute('''
        INSERT OR REPLACE INTO term_settings (school_id, current_academic_year, current_term, updated_at)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
    ''', (nanjati_id, target_year, target_term))

    # 3. Restore Settings
    if os.path.exists(SETTINGS_JSON):
        with open(SETTINGS_JSON, 'r', encoding='utf-8') as f:
            settings = json.load(f)
        total_grant = settings.get('totalGrantsByYear', {}).get(target_year, 0)
        cursor.execute('''
            INSERT OR REPLACE INTO school_settings 
            (school_id, academic_year, term, financial_year, school_name, school_address, 
             ministry_department, total_grant, balance_bf,
             compiled_by, entered_by, authorizing_officer, authorizing_appointment,
             counter_sign, counter_appointment, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (
            nanjati_id, target_year, target_term, legacy_fy, "NANJATI CDSS",
            settings.get('schoolAddress', ''),
            settings.get('ministry', 'Education'),
            total_grant,
            settings.get('balanceBF', 0),
            settings.get('compiledBy', ''),
            settings.get('enteredBy', ''),
            settings.get('authorizingOfficer', ''),
            settings.get('authorizingAppointment', ''),
            settings.get('counterSign', ''),
            settings.get('counterAppointment', '')
        ))

    # 4. Restore Budget Items (With Template ID fix)
    if os.path.exists(BUDGETS_JSON):
        with open(BUDGETS_JSON, 'r', encoding='utf-8') as f:
            budgets = json.load(f)
        
        items_count = 0
        fallback_counter = 100 # For non-standard items
        
        for budget in budgets:
            json_school_name = budget.get('schoolName', '').upper()
            target_id = nanjati_id if "NANJATI" in json_school_name else name_to_id.get(json_school_name)
            
            if target_id:
                for item in budget.get('items', []):
                    # Derive template_row_id if missing
                    tid = item.get('template_row_id')
                    if tid is None:
                        tid = find_template_id(item.get('powNo'), item.get('subItemDescription'), item.get('code'))
                    
                    if tid is None:
                        tid = fallback_counter
                        fallback_counter += 1
                    
                    cursor.execute('''
                        INSERT OR REPLACE INTO budget_items
                        (school_id, academic_year, term, financial_year, template_row_id, item_key, pow_no, pow_name, 
                         sub_activity, sub_item_description, code, total_allocation, monthly_allocations, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                    ''', (
                        target_id, target_year, target_term, legacy_fy,
                        tid,
                        item.get('id'),
                        item.get('powNo'),
                        item.get('powName'),
                        item.get('subActivity'),
                        item.get('subItemDescription'),
                        item.get('code'),
                        item.get('totalAllocation', 0),
                        json.dumps(item.get('monthlyAllocations', {}))
                    ))
                    items_count += 1
        print(f"✅ Restored {items_count} budget items.")

    # 5. Restore Credits & Debits
    if os.path.exists(CREDITS_JSON):
        with open(CREDITS_JSON, 'r', encoding='utf-8') as f:
            credits_data = json.load(f)
        for credit in credits_data:
            cursor.execute('''
                INSERT INTO credits (school_id, academic_year, term, financial_year, date_received, month, line_items, remarks, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (nanjati_id, target_year, target_term, legacy_fy, credit.get('date'), credit.get('month'), json.dumps(credit.get('lineItems', [])), credit.get('remarks', '')))

    if os.path.exists(DEBITS_JSON):
        with open(DEBITS_JSON, 'r', encoding='utf-8') as f:
            debits_data = json.load(f)
        for debit in debits_data:
            cursor.execute('''
                INSERT OR REPLACE INTO debits (school_id, academic_year, term, financial_year, document_number, date_paid, month, item_id,
                 sub_item_description, code, description, amount, amount_words, supplier_name, position, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (nanjati_id, target_year, target_term, legacy_fy, debit.get('documentNumber', ''), debit.get('date'), debit.get('month'), debit.get('itemId'),
                debit.get('subItemDescription'), debit.get('code'), debit.get('description'), debit.get('amount', 0), debit.get('amountWords', ''), debit.get('supplierName', ''), debit.get('position', '')))

    conn.commit()
    conn.close()
    print("\n🏁 RESTORATION COMPLETE!")

if __name__ == '__main__':
    restore_data()
