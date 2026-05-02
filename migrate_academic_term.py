
import sqlite3
import os

# Use absolute path to ensure same database file is always used
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DATABASE_PATH = os.path.join(DATA_DIR, 'grant_management.db')

def migrate():
    print(f"Starting migration on {DATABASE_PATH}...")
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # 1. Create system_settings table for tracking current term/year per school
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
    print("✅ Created term_settings table")

    # 2. Add academic_year and term to data tables
    tables = ['budget_items', 'credits', 'debits', 'financial_year_counters', 'ipdc_counters', 'school_settings']
    
    for table in tables:
        print(f"Migrating table: {table}")
        
        # Add academic_year
        try:
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN academic_year TEXT")
            print(f"  Added academic_year to {table}")
        except sqlite3.OperationalError:
            print(f"  academic_year already exists in {table}")
            
        # Add term
        try:
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN term TEXT")
            print(f"  Added term to {table}")
        except sqlite3.OperationalError:
            print(f"  term already exists in {table}")

    # 3. Backfill existing data
    # We'll use the existing financial_year as academic_year and 'Term 1' as default term
    for table in tables:
        # Check if financial_year column exists in this table
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'financial_year' in columns:
            cursor.execute(f"UPDATE {table} SET academic_year = financial_year WHERE academic_year IS NULL")
            cursor.execute(f"UPDATE {table} SET term = 'Term 1' WHERE term IS NULL")
            print(f"  Backfilled {table} with existing financial_year and 'Term 1'")
        else:
            # For tables without financial_year (if any were in my list but shouldn't be)
            cursor.execute(f"UPDATE {table} SET academic_year = '2026-2027' WHERE academic_year IS NULL")
            cursor.execute(f"UPDATE {table} SET term = 'Term 1' WHERE term IS NULL")
            print(f"  Backfilled {table} with defaults")

    # 4. Initialize term_settings for existing schools
    cursor.execute("SELECT id FROM schools")
    schools = cursor.fetchall()
    for school in schools:
        school_id = school[0]
        cursor.execute('''
            INSERT OR IGNORE INTO term_settings (school_id, current_academic_year, current_term)
            VALUES (?, '2026-2027', 'Term 1')
        ''', (school_id,))
    print(f"✅ Initialized term_settings for {len(schools)} schools")

    conn.commit()
    conn.close()
    print("🚀 Migration complete!")

if __name__ == "__main__":
    migrate()
