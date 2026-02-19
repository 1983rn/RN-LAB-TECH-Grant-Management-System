"""
Database helper functions for multi-tenant grant management
Replaces JSON file operations with proper database queries
"""
import json
from database import get_db

def get_school_settings(school_id, financial_year):
    """Get settings for specific school and financial year"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM school_settings
            WHERE school_id = ? AND financial_year = ?
        ''', (school_id, financial_year))
        row = cursor.fetchone()
        
        if row:
            return dict(row)
        
        # Return defaults if not found
        return {
            'school_id': school_id,
            'financial_year': financial_year,
            'school_name': '',
            'school_address': '',
            'ministry_department': 'Education',
            'total_grant': 0,
            'compiled_by': '',
            'entered_by': '',
            'authorizing_officer': '',
            'authorizing_appointment': '',
            'counter_sign': '',
            'counter_appointment': ''
        }

def save_school_settings(school_id, financial_year, settings_data):
    """Save settings for specific school and financial year"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO school_settings
            (school_id, financial_year, school_name, school_address, ministry_department, total_grant,
             compiled_by, entered_by, authorizing_officer, authorizing_appointment,
             counter_sign, counter_appointment, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (
            school_id,
            financial_year,
            settings_data.get('schoolName', ''),
            settings_data.get('schoolAddress', ''),
            settings_data.get('ministry', 'Education'),
            settings_data.get('totalGrant', 0),
            settings_data.get('compiledBy', ''),
            settings_data.get('enteredBy', ''),
            settings_data.get('authorizingOfficer', ''),
            settings_data.get('authorizingAppointment', ''),
            settings_data.get('counterSign', ''),
            settings_data.get('counterAppointment', '')
        ))
    return True

def get_school_budget(school_id, financial_year):
    """Get budget for specific school and financial year"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM budget_items
            WHERE school_id = ? AND financial_year = ?
            ORDER BY template_row_id
        ''', (school_id, financial_year))
        rows = cursor.fetchall()
        
        if not rows:
            return None
        
        items = []
        for row in rows:
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
        
        return {
            'financialYear': financial_year,
            'items': items
        }

def save_school_budget(school_id, financial_year, budget_data):
    """Save budget for specific school and financial year - INSERT OR REPLACE"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Use INSERT OR REPLACE to handle both new and existing rows
            for item in budget_data.get('items', []):
                template_row_id = item.get('template_row_id')
                if not template_row_id:
                    continue
                
                cursor.execute('''
                    INSERT OR REPLACE INTO budget_items
                    (school_id, financial_year, template_row_id, item_key, pow_no, pow_name, 
                     sub_activity, sub_item_description, code, total_allocation, monthly_allocations)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    school_id,
                    financial_year,
                    template_row_id,
                    item.get('id'),
                    item.get('powNo'),
                    item.get('powName'),
                    item.get('subActivity'),
                    item.get('subItemDescription'),
                    item.get('code'),
                    item.get('totalAllocation', 0),
                    json.dumps(item.get('monthlyAllocations', {}))
                ))
        return True
    except Exception as e:
        print(f"ERROR in save_school_budget: {e}")
        import traceback
        traceback.print_exc()
        return False

def get_school_credits(school_id, financial_year):
    """Get credits for specific school and financial year"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM credits
            WHERE school_id = ? AND financial_year = ?
            ORDER BY date_received DESC
        ''', (school_id, financial_year))
        rows = cursor.fetchall()
        
        credits = []
        for row in rows:
            credit = {
                'id': f"credit_{row['id']}",
                'date': row['date_received'],
                'month': row['month'],
                'lineItems': json.loads(row['line_items']),
                'remarks': row['remarks'],
                'financialYear': row['financial_year']
            }
            credits.append(credit)
        
        return credits

def save_school_credit(school_id, financial_year, credit_data):
    """Save credit for specific school"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO credits
            (school_id, financial_year, date_received, month, line_items, remarks)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            school_id, financial_year,
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

def get_school_debits(school_id, financial_year):
    """Get debits for specific school and financial year"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM debits
            WHERE school_id = ? AND financial_year = ?
            ORDER BY date_paid DESC
        ''', (school_id, financial_year))
        rows = cursor.fetchall()
        
        debits = []
        for row in rows:
            debit = {
                'id': f"debit_{row['id']}",
                'documentNumber': row['document_number'],
                'date': row['date_paid'],
                'month': row['month'],
                'itemId': row['item_id'],
                'subItemDescription': row['sub_item_description'],
                'code': row['code'],
                'description': row['description'],
                'amount': row['amount'],
                'amountWords': row['amount_words'],
                'supplierName': row['supplier_name'],
                'position': row['position'],
                'looseMinuteNumber': row['loose_minute_number'],
                'receiptNumber': row['receipt_number'],
                'financialYear': row['financial_year']
            }
            debits.append(debit)
        
        return debits

def save_school_debit(school_id, financial_year, debit_data):
    """Save debit for specific school"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO debits
            (school_id, financial_year, document_number, date_paid, month, item_id,
             sub_item_description, code, description, amount, amount_words,
             supplier_name, position, loose_minute_number, receipt_number)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            school_id, financial_year,
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
            debit_data.get('looseMinuteNumber', ''),
            debit_data.get('receiptNumber', '')
        ))
        return cursor.lastrowid

def update_school_debit(school_id, debit_id, updates):
    """Update debit for specific school"""
    numeric_id = int(debit_id.replace('debit_', ''))
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Build update query dynamically
        fields = []
        values = []
        
        if 'looseMinuteNumber' in updates:
            fields.append('loose_minute_number = ?')
            values.append(updates['looseMinuteNumber'])
        if 'receiptNumber' in updates:
            fields.append('receipt_number = ?')
            values.append(updates['receiptNumber'])
        
        if fields:
            values.extend([numeric_id, school_id])
            query = f"UPDATE debits SET {', '.join(fields)} WHERE id = ? AND school_id = ?"
            cursor.execute(query, values)
    return True

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

def get_next_document_number(school_id, financial_year, doc_type):
    """Get next sequential document number for school"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Get current max number from debits table
        if doc_type == 'gp10':
            cursor.execute('''
                SELECT MAX(CAST(document_number AS INTEGER)) as max_no
                FROM debits
                WHERE school_id = ? AND financial_year = ?
                AND document_number GLOB '[0-9]*'
            ''', (school_id, financial_year))
        elif doc_type == 'looseMinute':
            cursor.execute('''
                SELECT MAX(CAST(loose_minute_number AS INTEGER)) as max_no
                FROM debits
                WHERE school_id = ? AND financial_year = ?
                AND loose_minute_number GLOB '[0-9]*'
            ''', (school_id, financial_year))
        elif doc_type == 'receipt':
            cursor.execute('''
                SELECT MAX(CAST(receipt_number AS INTEGER)) as max_no
                FROM debits
                WHERE school_id = ? AND financial_year = ?
                AND receipt_number GLOB '[0-9]*'
            ''', (school_id, financial_year))
        
        row = cursor.fetchone()
        max_no = row['max_no'] if row and row['max_no'] else 0
        next_no = max_no + 1
        
        return f"{next_no:04d}"
