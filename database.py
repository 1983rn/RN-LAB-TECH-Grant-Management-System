"""
Multi-Tenant Database Schema and Management
"""
import sqlite3
import hashlib
import secrets
import os
from datetime import datetime, timedelta
from contextlib import contextmanager

# Use absolute path to ensure same database file is always used
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DATABASE_PATH = os.path.join(DATA_DIR, 'grant_management.db')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

print(f"Database location: {DATABASE_PATH}")

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, password_hash):
    """Verify password against hash"""
    return hash_password(password) == password_hash

@contextmanager
def get_db():
    """Database connection context manager with WAL mode and busy timeout"""
    conn = sqlite3.connect(DATABASE_PATH, timeout=30.0, isolation_level=None)
    conn.row_factory = sqlite3.Row
    # Enable WAL mode for better concurrency
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('PRAGMA synchronous=NORMAL')
    conn.execute('PRAGMA busy_timeout=30000')
    conn.execute('PRAGMA wal_autocheckpoint=1000')
    try:
        yield conn
        # Force checkpoint to ensure data is written to main database file
        conn.execute('PRAGMA wal_checkpoint(PASSIVE)')
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_database():
    """Initialize multi-tenant database schema"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Enable WAL mode for better concurrency (persistent setting)
        cursor.execute('PRAGMA journal_mode=WAL')
        cursor.execute('PRAGMA synchronous=NORMAL')
        
        # Schools table (tenants)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schools (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                school_name TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                is_locked BOOLEAN DEFAULT 0,
                subscription_type TEXT DEFAULT 'TRIAL',
                subscription_start DATE,
                subscription_end DATE,
                expiry_date DATE,
                subscription_status TEXT DEFAULT 'UNPAID',
                last_login DATETIME,
                last_activity DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Add missing columns if they don't exist (migration)
        try:
            cursor.execute('ALTER TABLE schools ADD COLUMN subscription_type TEXT DEFAULT "TRIAL"')
            print("✅ Added subscription_type column")
        except:
            pass  # Column already exists
        
        try:
            cursor.execute('ALTER TABLE schools ADD COLUMN expiry_date DATE')
            print("✅ Added expiry_date column")
        except:
            pass  # Column already exists
        
        try:
            cursor.execute('ALTER TABLE schools ADD COLUMN last_activity DATETIME')
            print("✅ Added last_activity column")
        except:
            pass  # Column already exists
        
        # School settings per financial year
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS school_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                school_id INTEGER NOT NULL,
                academic_year TEXT NOT NULL,
                term TEXT NOT NULL,
                financial_year TEXT NOT NULL,
                school_name TEXT,
                school_address TEXT,
                ministry_department TEXT DEFAULT 'Education',
                total_grant REAL DEFAULT 0,
                balance_bf REAL DEFAULT 0,
                compiled_by TEXT,
                entered_by TEXT,
                authorizing_officer TEXT,
                authorizing_appointment TEXT,
                counter_sign TEXT,
                counter_appointment TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (school_id) REFERENCES schools(id),
                UNIQUE(school_id, academic_year, term)
            )
        ''')
        
        # Budget allocation (multi-tenant) - template_row_id ensures uniqueness
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS budget_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                school_id INTEGER NOT NULL,
                academic_year TEXT NOT NULL,
                term TEXT NOT NULL,
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
                UNIQUE(school_id, academic_year, term, template_row_id)
            )
        ''')
        
        # Credit register (multi-tenant)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS credits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                school_id INTEGER NOT NULL,
                academic_year TEXT NOT NULL,
                term TEXT NOT NULL,
                financial_year TEXT NOT NULL,
                date_received DATE NOT NULL,
                month TEXT NOT NULL,
                line_items TEXT NOT NULL,
                remarks TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (school_id) REFERENCES schools(id)
            )
        ''')
        
        # Debit register (multi-tenant) - unified document numbers
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS debits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                school_id INTEGER NOT NULL,
                academic_year TEXT NOT NULL,
                term TEXT NOT NULL,
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
                cheque_number TEXT,
                ipdc_venue TEXT,
                ipdc_minute_no TEXT,
                ipdc_members TEXT,
                ipdc_opening_prayer TEXT,
                ipdc_closing_prayer TEXT,
                ipdc_quotations TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (school_id) REFERENCES schools(id)
            )
        ''')
        
        # Create unique index to prevent duplicate transaction numbers
        cursor.execute('''
            CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_transaction
            ON debits (school_id, academic_year, term, document_number)
        ''')
        
        # Financial year counters - persistent sequential numbering
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS financial_year_counters (
                school_id INTEGER NOT NULL,
                academic_year TEXT NOT NULL,
                term TEXT NOT NULL,
                financial_year TEXT,
                last_number INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (school_id, academic_year, term)
            )
        ''')
        
        # IPDC counters - sequential numbering for IPDC minutes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ipdc_counters (
                school_id INTEGER NOT NULL,
                academic_year TEXT NOT NULL,
                term TEXT NOT NULL,
                financial_year TEXT,
                last_number INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (school_id, academic_year, term)
            )
        ''')
        
        # Subscription messages
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscription_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                school_id INTEGER NOT NULL,
                message TEXT NOT NULL,
                message_type TEXT DEFAULT 'INFO',
                is_read BOOLEAN DEFAULT 0,
                sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (school_id) REFERENCES schools(id)
            )
        ''')

        # Term settings (Control Center)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS term_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                school_id INTEGER NOT NULL,
                current_academic_year TEXT NOT NULL,
                current_term TEXT NOT NULL,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (school_id) REFERENCES schools(id),
                UNIQUE(school_id)
            )
        ''')
        
        # School sessions (online tracking)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS school_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                school_id INTEGER NOT NULL,
                login_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
                is_online BOOLEAN DEFAULT 1,
                FOREIGN KEY (school_id) REFERENCES schools(id)
            )
        ''')
        
        # Password reset tokens
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS password_reset_tokens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                school_id INTEGER NOT NULL,
                otp_code TEXT NOT NULL,
                expires_at DATETIME NOT NULL,
                used BOOLEAN DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (school_id) REFERENCES schools(id)
            )
        ''')
        
        # Audit logs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                actor_type TEXT NOT NULL,
                actor_id TEXT NOT NULL,
                action TEXT NOT NULL,
                target_school_id INTEGER,
                ip_address TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (target_school_id) REFERENCES schools(id)
            )
        ''')
        
        # Create indexes for performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_budget_school ON budget_items(school_id, financial_year)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_credits_school ON credits(school_id, financial_year)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_debits_school ON debits(school_id, financial_year)')
        
        # IPDC Column Migrations - Robust check
        def column_exists(table, column):
            cursor.execute(f"PRAGMA table_info({table})")
            return any(row[1] == column for row in cursor.fetchall())

        columns_to_add = [
            ('debits', 'ipdc_venue', 'TEXT'),
            ('debits', 'ipdc_minute_no', 'TEXT'),
            ('debits', 'ipdc_members', 'TEXT'),
            ('debits', 'ipdc_opening_prayer', 'TEXT'),
            ('debits', 'ipdc_closing_prayer', 'TEXT'),
            ('debits', 'ipdc_quotations', 'TEXT'),
            ('debits', 'cheque_number', 'TEXT')
        ]

        for table, col, col_type in columns_to_add:
            if not column_exists(table, col):
                try:
                    cursor.execute(f'ALTER TABLE {table} ADD COLUMN {col} {col_type}')
                    print(f"✅ Added {col} column to {table}")
                except Exception as e:
                    print(f"❌ Error adding {col} to {table}: {e}")

        # Add academic_year and term to all data tables if missing
        for table in ['budget_items', 'credits', 'debits', 'financial_year_counters', 'ipdc_counters', 'school_settings']:
            for col in [('academic_year', 'TEXT'), ('term', 'TEXT')]:
                if not column_exists(table, col[0]):
                    try:
                        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {col[0]} {col[1]}")
                        print(f"✅ Added {col[0]} to {table}")
                    except Exception as e:
                        print(f"❌ Error adding {col[0]} to {table}: {e}")
        
        # Specific column additions
        if not column_exists('school_settings', 'balance_bf'):
            try:
                cursor.execute("ALTER TABLE school_settings ADD COLUMN balance_bf REAL DEFAULT 0")
                print("✅ Added balance_bf to school_settings")
            except Exception as e:
                print(f"❌ Error adding balance_bf: {e}")


        cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_school ON school_sessions(school_id)')
        
        print("✅ Multi-tenant database initialized successfully")

def create_developer_account():
    """Create developer account if not exists"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM schools WHERE username = ?', ('juniornsambe@yahoo.com',))
        if not cursor.fetchone():
            password_hash = hash_password('blessings19831983/')
            cursor.execute('''
                INSERT INTO schools (school_name, username, password_hash, is_active, subscription_status)
                VALUES (?, ?, ?, ?, ?)
            ''', ('DEVELOPER_ACCOUNT', 'juniornsambe@yahoo.com', password_hash, 1, 'LIFETIME'))
            print("✅ Developer account created")

def log_action(actor_type, actor_id, action, target_school_id=None, ip_address=None):
    """Log audit action - never fails, just logs errors"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO audit_logs (actor_type, actor_id, action, target_school_id, ip_address)
                VALUES (?, ?, ?, ?, ?)
            ''', (actor_type, actor_id, action, target_school_id, ip_address))
    except Exception as e:
        print(f"Warning: Failed to log action: {e}")
        # Don't raise - logging failure should not break the application

def generate_otp():
    """Generate 6-digit OTP"""
    return ''.join([str(secrets.randbelow(10)) for _ in range(6)])

if __name__ == '__main__':
    init_database()
    create_developer_account()
