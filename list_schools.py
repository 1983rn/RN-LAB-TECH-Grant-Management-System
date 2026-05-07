import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data', 'grant_management.db')

def list_schools():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("--- SCHOOLS ---")
    cursor.execute("SELECT id, school_name, username, created_at FROM schools")
    schools = cursor.fetchall()
    for school in schools:
        print(f"ID: {school['id']}, Name: {school['school_name']}, Username: {school['username']}, Created: {school['created_at']}")
    
    print("\n--- TERM SETTINGS ---")
    cursor.execute("SELECT school_id, current_academic_year, current_term FROM term_settings")
    terms = cursor.fetchall()
    for term in terms:
        print(f"School ID: {term['school_id']}, Year: {term['current_academic_year']}, Term: {term['current_term']}")

    print("\n--- BUDGET COUNT ---")
    cursor.execute("SELECT school_id, academic_year, term, COUNT(*) as count FROM budget_items GROUP BY school_id, academic_year, term")
    counts = cursor.fetchall()
    for c in counts:
        print(f"School ID: {c['school_id']}, Year: {c['academic_year']}, Term: {c['term']}, Items: {c['count']}")

    conn.close()

if __name__ == '__main__':
    list_schools()
