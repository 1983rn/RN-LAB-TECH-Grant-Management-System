"""
Add school_name column to existing school_settings table
"""
from database import get_db

def add_school_name_column():
    """Add school_name column if it doesn't exist"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Check if column exists
            cursor.execute("PRAGMA table_info(school_settings)")
            columns = [row[1] for row in cursor.fetchall()]
            
            if 'school_name' not in columns:
                print("Adding school_name column to school_settings table...")
                cursor.execute("ALTER TABLE school_settings ADD COLUMN school_name TEXT")
                print("✅ Column added successfully!")
            else:
                print("✅ school_name column already exists")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    add_school_name_column()
