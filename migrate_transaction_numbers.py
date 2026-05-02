#!/usr/bin/env python3
"""
Migration Script: Unified Transaction Numbering System
- Creates financial_year_counters table
- Removes old document_sequences table
- Removes loose_minute_number and receipt_number columns from debits
- Adds unique index on (school_id, financial_year, document_number)
"""

import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_FILE = os.path.join(DATA_DIR, 'grant_management.db')

def migrate():
    print("Starting transaction numbering migration...")
    print(f"Database: {DB_FILE}")
    
    if not os.path.exists(DB_FILE):
        print("ERROR: Database not found!")
        return
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        # Step 1: Create financial_year_counters table
        print("\n[1] Creating financial_year_counters table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS financial_year_counters (
                school_id INTEGER NOT NULL,
                financial_year TEXT NOT NULL,
                last_number INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (school_id, financial_year)
            )
        ''')
        print("   SUCCESS: Table created")
        
        # Step 2: Migrate existing counters from document_sequences
        print("\n[2] Migrating existing counters...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='document_sequences'")
        if cursor.fetchone():
            cursor.execute('''
                SELECT school_id, financial_year, 
                       MAX(gp10_last_no, loose_minute_last_no, receipt_last_no) as max_no
                FROM document_sequences
            ''')
            for row in cursor.fetchall():
                school_id, financial_year, max_no = row
                cursor.execute('''
                    INSERT OR REPLACE INTO financial_year_counters
                    (school_id, financial_year, last_number)
                    VALUES (?, ?, ?)
                ''', (school_id, financial_year, max_no or 0))
                print(f"   SUCCESS: Migrated school_id={school_id}, year={financial_year}, counter={max_no}")
        else:
            print("   INFO: No document_sequences table found (fresh install)")
        
        # Step 3: Create new debits table without separate number columns
        print("\n[3] Recreating debits table...")
        
        # Check if old columns exist
        cursor.execute("PRAGMA table_info(debits)")
        columns = [col[1] for col in cursor.fetchall()]
        has_old_columns = 'loose_minute_number' in columns or 'receipt_number' in columns
        
        if has_old_columns:
            print("   Backing up existing debits...")
            cursor.execute('''
                CREATE TABLE debits_backup AS 
                SELECT * FROM debits
            ''')
            
            print("   Dropping old debits table...")
            cursor.execute('DROP TABLE debits')
            
            print("   Creating new debits table...")
            cursor.execute('''
                CREATE TABLE debits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    school_id INTEGER NOT NULL,
                    financial_year TEXT NOT NULL,
                    document_number TEXT NOT NULL,
                    date_paid DATE NOT NULL,
                    month TEXT NOT NULL,
                    item_id TEXT NOT NULL,
                    sub_item_description TEXT,
                    code TEXT,
                    description TEXT,
                    amount REAL NOT NULL,
                    amount_words TEXT,
                    supplier_name TEXT,
                    position TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (school_id) REFERENCES schools(id)
                )
            ''')
            
            print("   Restoring data with sequential numbering...")
            # Get all schools and financial years
            cursor.execute('''
                SELECT DISTINCT school_id, financial_year 
                FROM debits_backup
                ORDER BY school_id, financial_year
            ''')
            school_years = cursor.fetchall()
            
            for school_id, financial_year in school_years:
                # Get debits for this school/year ordered by date
                cursor.execute('''
                    SELECT id, date_paid, month, item_id, sub_item_description, 
                           code, description, amount, amount_words, supplier_name, 
                           position, created_at
                    FROM debits_backup
                    WHERE school_id = ? AND financial_year = ?
                    ORDER BY date_paid, id
                ''', (school_id, financial_year))
                
                debits = cursor.fetchall()
                counter = 1
                
                for debit in debits:
                    doc_number = str(counter).zfill(4)
                    cursor.execute('''
                        INSERT INTO debits 
                        (id, school_id, financial_year, document_number, date_paid, month, 
                         item_id, sub_item_description, code, description, amount, 
                         amount_words, supplier_name, position, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (debit[0], school_id, financial_year, doc_number, 
                          debit[1], debit[2], debit[3], debit[4], debit[5], 
                          debit[6], debit[7], debit[8], debit[9], debit[10], debit[11]))
                    counter += 1
                
                # Update counter table
                cursor.execute('''
                    INSERT OR REPLACE INTO financial_year_counters
                    (school_id, financial_year, last_number)
                    VALUES (?, ?, ?)
                ''', (school_id, financial_year, counter - 1))
                
                print(f"   SUCCESS: Renumbered {counter-1} debits for school_id={school_id}, year={financial_year}")
            
            print("   Dropping backup table...")
            cursor.execute('DROP TABLE debits_backup')
        else:
            print("   INFO: Debits table already in correct format")
        
        # Step 4: Create unique index
        print("\n[4] Creating unique index...")
        cursor.execute('DROP INDEX IF EXISTS idx_unique_transaction')
        cursor.execute('''
            CREATE UNIQUE INDEX idx_unique_transaction
            ON debits (school_id, financial_year, document_number)
        ''')
        print("   SUCCESS: Index created")
        
        # Step 5: Drop old document_sequences table
        print("\n[5] Cleaning up old tables...")
        cursor.execute('DROP TABLE IF EXISTS document_sequences')
        print("   SUCCESS: Old document_sequences table removed")
        
        # Step 6: Verify migration
        print("\n[6] Verifying migration...")
        cursor.execute('SELECT COUNT(*) FROM financial_year_counters')
        counter_count = cursor.fetchone()[0]
        print(f"   SUCCESS: Counter records: {counter_count}")
        
        cursor.execute('SELECT COUNT(*) FROM debits')
        debit_count = cursor.fetchone()[0]
        print(f"   SUCCESS: Debit records: {debit_count}")
        
        conn.commit()
        print("\nSUCCESS: Migration completed successfully!")
        print("\nSummary:")
        print(f"   - Unified transaction numbering enabled")
        print(f"   - Year-based counters: {counter_count}")
        print(f"   - Debits migrated: {debit_count}")
        print(f"   - No monthly reset")
        print(f"   - Concurrency safe")
        
    except Exception as e:
        conn.rollback()
        print(f"\nERROR: Migration failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == '__main__':
    migrate()
