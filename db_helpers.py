"""
Database helper functions for multi-tenant grant management
Replaces JSON file operations with proper database queries
"""
import json
import datetime
from database import get_db

def get_term_settings(school_id):
    """Get current academic year and term settings for a school"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT current_academic_year, current_term 
            FROM term_settings 
            WHERE school_id = ?
        ''', (school_id,))
        row = cursor.fetchone()
        
        if row:
            return dict(row)
        
        # Default if not set
        return {
            'current_academic_year': '2026-2027',
            'current_term': 'Term 1'
        }

def save_term_settings(school_id, academic_year, term):
    """Save current academic year and term settings for a school"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO term_settings 
            (school_id, current_academic_year, current_term, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        ''', (school_id, academic_year, term))
    return True

def get_school_settings(school_id, academic_year, term):
    """Get settings for specific school, academic year and term"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM school_settings
            WHERE school_id = ? AND academic_year = ? AND term = ?
        ''', (school_id, academic_year, term))
        row = cursor.fetchone()
        
        if row:
            return dict(row)
        
        # Return defaults if not found
        return {
            'school_id': school_id,
            'academic_year': academic_year,
            'term': term,
            'school_name': '',
            'school_address': '',
            'ministry_department': 'Education',
            'total_grant': 0,
            'balance_bf': 0,
            'compiled_by': '',
            'entered_by': '',
            'authorizing_officer': '',
            'authorizing_appointment': '',
            'counter_sign': '',
            'counter_appointment': ''
        }

def save_school_settings(school_id, academic_year, term, settings_data):
    """Save settings for specific school, academic year and term"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO school_settings
            (school_id, academic_year, term, financial_year, school_name, school_address, 
             ministry_department, total_grant, balance_bf, compiled_by, entered_by, 
             authorizing_officer, authorizing_appointment, counter_sign, 
             counter_appointment, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (
            school_id,
            academic_year,
            term,
            f"{academic_year}_{term}", # Combined for legacy UNIQUE constraint
            settings_data.get('schoolName', ''),
            settings_data.get('schoolAddress', ''),
            settings_data.get('ministry', 'Education'),
            settings_data.get('totalGrant', 0),
            settings_data.get('balanceBF', 0),
            settings_data.get('compiledBy', ''),
            settings_data.get('enteredBy', ''),
            settings_data.get('authorizingOfficer', ''),
            settings_data.get('authorizingAppointment', ''),
            settings_data.get('counterSign', ''),
            settings_data.get('counterAppointment', '')
        ))
    return True

def get_school_budget(school_id, academic_year, term):
    """Get budget for specific school, academic year and term"""
    print(f"\n=== GET SCHOOL BUDGET DEBUG ===")
    print(f"School ID: {school_id}")
    print(f"Academic Year: {academic_year}")
    print(f"Term: {term}")
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM budget_items
            WHERE school_id = ? AND academic_year = ? AND term = ?
            ORDER BY template_row_id
        ''', (school_id, academic_year, term))
        rows = cursor.fetchall()
        
        print(f"Found {len(rows)} budget items in database")
        
        if not rows:
            print("No budget items found - returning None")
            print("=== GET SCHOOL BUDGET COMPLETE ===\n")
            return None
        
        items = []
        for i, row in enumerate(rows):
            item = dict(row)
            item['id'] = item['item_key']
            item['template_row_id'] = item['template_row_id']
            item['powNo'] = item['pow_no']
            item['powName'] = item['pow_name']
            item['subActivity'] = item['sub_activity']
            item['subItemDescription'] = item['sub_item_description']
            item['totalAllocation'] = item['total_allocation']
            item['monthlyAllocations'] = json.loads(item['monthly_allocations']) if item['monthly_allocations'] else {}
            items.append(item)
            
            if i < 3:  # Log first 3 items
                print(f"  Item {i}: template_row_id={item['template_row_id']}, allocation={item['totalAllocation']}")
        
        result = {
            'academicYear': academic_year,
            'term': term,
            'items': items
        }
        print(f"Returning budget with {len(items)} items")
        print("=== GET SCHOOL BUDGET COMPLETE ===\n")
        return result

def save_school_budget(school_id, academic_year, term, budget_data):
    """Save budget for specific school, academic year and term - INSERT OR REPLACE"""
    try:
        print(f"\n=== SAVE SCHOOL BUDGET DEBUG ===")
        print(f"School ID: {school_id}")
        print(f"Academic Year: {academic_year}")
        print(f"Term: {term}")
        print(f"Items to save: {len(budget_data.get('items', []))}")
        
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Use INSERT OR REPLACE to handle both new and existing rows
            for i, item in enumerate(budget_data.get('items', [])):
                template_row_id = item.get('template_row_id')
                if not template_row_id:
                    print(f"WARNING: Item {i} missing template_row_id, skipping")
                    continue
                
                allocation = item.get('totalAllocation', 0)
                if i < 3:  # Log first 3 items
                    print(f"  Item {i}: template_row_id={template_row_id}, allocation={allocation}")
                
                cursor.execute('''
                    INSERT OR REPLACE INTO budget_items
                    (school_id, academic_year, term, financial_year, template_row_id, item_key, pow_no, pow_name, 
                     sub_activity, sub_item_description, code, total_allocation, monthly_allocations)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    school_id,
                    academic_year,
                    term,
                    f"{academic_year}_{term}", # Combined for legacy UNIQUE constraint
                    template_row_id,
                    item.get('id'),
                    item.get('powNo'),
                    item.get('powName'),
                    item.get('subActivity'),
                    item.get('subItemDescription'),
                    item.get('code'),
                    allocation,
                    json.dumps(item.get('monthlyAllocations', {}))
                ))
            
            # Verify data was written
            cursor.execute('''
                SELECT COUNT(*) FROM budget_items 
                WHERE school_id = ? AND academic_year = ? AND term = ?
            ''', (school_id, academic_year, term))
            count = cursor.fetchone()[0]
            print(f"Database now has {count} budget items for this school/year/term")
            
        print("=== SAVE SCHOOL BUDGET COMPLETE ===\n")
        return True
    except Exception as e:
        print(f"ERROR in save_school_budget: {e}")
        import traceback
        traceback.print_exc()
        return False

def get_school_credits(school_id, academic_year, term):
    """Get credits for specific school, academic year and term"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM credits
            WHERE school_id = ? AND academic_year = ? AND term = ?
            ORDER BY date_received DESC
        ''', (school_id, academic_year, term))
        rows = cursor.fetchall()
        
        credits = []
        for row in rows:
            credit = {
                'id': f"credit_{row['id']}",
                'date': row['date_received'],
                'month': row['month'],
                'lineItems': json.loads(row['line_items']),
                'remarks': row['remarks'],
                'academicYear': row['academic_year'],
                'term': row['term']
            }
            credits.append(credit)
        
        return credits

def save_school_credit(school_id, academic_year, term, credit_data):
    """Save credit for specific school"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO credits
            (school_id, academic_year, term, financial_year, date_received, month, line_items, remarks)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            school_id, academic_year, term,
            f"{academic_year}_{term}", # Combined for legacy UNIQUE constraint
            credit_data.get('date'),
            credit_data.get('month'),
            json.dumps(credit_data.get('lineItems', [])),
            credit_data.get('remarks', '')
        ))
    return True

def delete_school_credit(school_id, credit_id):
    """Delete credit for specific school"""
    # Extract numeric ID from credit_id (format: credit_123)
    numeric_id = int(credit_id.replace('credit_', ''))
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM credits
            WHERE id = ? AND school_id = ?
        ''', (numeric_id, school_id))
    return True

def get_school_debits(school_id, academic_year, term):
    """Get debits for specific school, academic year and term"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM debits
            WHERE school_id = ? AND academic_year = ? AND term = ?
            ORDER BY date_paid DESC
        ''', (school_id, academic_year, term))
        rows = cursor.fetchall()
        
        debits = []
        for row in rows:
            row_dict = dict(row)
            doc_num = row_dict.get('document_number', '0001')
            
            debit = {
                'id': f"debit_{row_dict['id']}",
                'documentNumber': doc_num,
                'date': row_dict['date_paid'],
                'month': row_dict['month'],
                'itemId': row_dict['item_id'],
                'subItemDescription': row_dict.get('sub_item_description'),
                'code': row_dict.get('code'),
                'description': row_dict.get('description'),
                'amount': row_dict['amount'],
                'amountWords': row_dict.get('amount_words'),
                'supplierName': row_dict.get('supplier_name'),
                'position': row_dict.get('position'),
                'looseMinuteNumber': doc_num,
                'gp10VoucherNumber': doc_num,
                'receiptNumber': doc_num,
                'academicYear': row_dict['academic_year'],
                'term': row_dict['term'],
                'chequeNumber': row_dict.get('cheque_number', ''),
                'ipdcVenue': row_dict.get('ipdc_venue', ''),
                'ipdcMinuteNo': row_dict.get('ipdc_minute_no', ''),
                'ipdcMembers': row_dict.get('ipdc_members', ''),
                'ipdcOpeningPrayer': row_dict.get('ipdc_opening_prayer', ''),
                'ipdcClosingPrayer': row_dict.get('ipdc_closing_prayer', '')
            }
            debits.append(debit)
        
        return debits

def save_school_debit(school_id, academic_year, term, debit_data):
    """Save debit with unified transaction number and term tagging"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO debits
            (school_id, academic_year, term, financial_year, document_number, date_paid, month, item_id,
             sub_item_description, code, description, amount, amount_words,
             supplier_name, position, cheque_number)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            school_id, academic_year, term,
            f"{academic_year}_{term}", # Combined for legacy UNIQUE constraint
            debit_data.get('documentNumber', ''),
            debit_data.get('date'),
            debit_data.get('month'),
            debit_data.get('itemId'),
            debit_data.get('subItemDescription'),
            debit_data.get('code'),
            debit_data.get('description'),
            debit_data.get('amount', 0),
            debit_data.get('amountWords', ''),
            debit_data.get('supplierName', ''),
            debit_data.get('position', ''),
            debit_data.get('chequeNumber', '')
        ))
        return cursor.lastrowid

def delete_school_debit(school_id, debit_id):
    """Delete debit for specific school"""
    numeric_id = int(debit_id.replace('debit_', ''))
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM debits
            WHERE id = ? AND school_id = ?
        ''', (numeric_id, school_id))
    return True

def generate_transaction_number(school_id, academic_year, term):
    """Generate sequential transaction number per term"""
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            # Query the maximum existing document number for this term
            cursor.execute('''
                SELECT MAX(CAST(document_number AS INTEGER))
                FROM debits
                WHERE school_id = ? AND academic_year = ? AND term = ?
            ''', (school_id, academic_year, term))
            
            result = cursor.fetchone()
            last_number = result[0] if result and result[0] is not None else 0
            new_number = last_number + 1
            
            return str(new_number).zfill(4)
        except Exception:
            raise


def get_next_document_number(school_id, academic_year, term, doc_type):
    """DEPRECATED: Use generate_transaction_number instead"""
    return generate_transaction_number(school_id, academic_year, term)

def initialize_budget_for_year(school_id, academic_year, term):
    """Auto-initialize budget structure for new academic year/term if not exists"""
    print(f"\n=== INITIALIZE BUDGET FOR TERM ===")
    print(f"School ID: {school_id}, Academic Year: {academic_year}, Term: {term}")
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM budget_items WHERE school_id = ? AND academic_year = ? AND term = ?',
                      (school_id, academic_year, term))
        count = cursor.fetchone()[0]
        
        print(f"Existing budget items: {count}")
        
        if count > 0:
            print("Budget already initialized, skipping")
            print("=== INITIALIZE COMPLETE ===\n")
            return
        
        print("No budget items found, creating template...")
        
        # Import here to avoid circular dependency
        import app
        template = app.generate_budget_structure()
        
        print(f"Inserting {len(template)} template rows...")
        
        for i, item in enumerate(template):
            cursor.execute('''
                INSERT INTO budget_items
                (school_id, academic_year, term, financial_year, template_row_id, item_key, pow_no, pow_name,
                 sub_activity, sub_item_description, code, total_allocation, monthly_allocations)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (school_id, academic_year, term, f"{academic_year}_{term}", item['template_row_id'], item['id'],
                  item['powNo'], item['powName'], item['subActivity'],
                  item['subItemDescription'], item['code'], 0,
                  json.dumps(item.get('monthlyAllocations', {}))))
            
            if i < 3:  # Log first 3
                print(f"  Inserted item {i}: template_row_id={item['template_row_id']}")
        
        # Verify
        cursor.execute('SELECT COUNT(*) FROM budget_items WHERE school_id = ? AND academic_year = ? AND term = ?',
                      (school_id, academic_year, term))
        final_count = cursor.fetchone()[0]
        print(f"Budget initialized successfully: {final_count} items created")
        print("=== INITIALIZE COMPLETE ===\n")

def generate_ipdc_number(school_id, academic_year, term):
    """Generate sequential number for IPDC minutes per term"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("BEGIN IMMEDIATE")
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO ipdc_counters
                (school_id, academic_year, term, financial_year, last_number)
                VALUES (?, ?, ?, ?, 0)
            ''', (school_id, academic_year, term, f"{academic_year}_{term}"))
            
            cursor.execute('''
                SELECT last_number FROM ipdc_counters
                WHERE school_id = ? AND academic_year = ? AND term = ?
            ''', (school_id, academic_year, term))
            
            last_number = cursor.fetchone()[0]
            new_number = last_number + 1
            
            cursor.execute('''
                UPDATE ipdc_counters
                SET last_number = ?
                WHERE school_id = ? AND academic_year = ? AND term = ?
            ''', (new_number, school_id, academic_year, term))
            
            conn.commit()
            return f"{str(new_number).zfill(3)}/{academic_year.split('-')[0]}"
        except Exception:
            conn.rollback()
            raise

def update_debit_ipdc_fields(school_id, debit_id, ipdc_data):
    """Update IPDC related fields for a specific debit"""
    numeric_id = int(debit_id.replace('debit_', ''))
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE debits
            SET ipdc_venue = ?,
                ipdc_minute_no = ?,
                ipdc_members = ?,
                ipdc_opening_prayer = ?,
                ipdc_closing_prayer = ?
            WHERE id = ? AND school_id = ?
        ''', (
            ipdc_data.get('venue', ''),
            ipdc_data.get('minute_no', ''),
            ipdc_data.get('members', ''),
            ipdc_data.get('opening_prayer', ''),
            ipdc_data.get('closing_prayer', ''),
            numeric_id,
            school_id
        ))
    return True

