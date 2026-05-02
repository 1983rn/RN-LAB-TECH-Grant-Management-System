import sqlite3

def clean_nanjati_pows():
    conn = sqlite3.connect('data/grant_management.db')
    cursor = conn.cursor()
    
    # Get NANJATI CDSS school_id
    cursor.execute("SELECT id FROM schools WHERE username = 'NANJATICDSS'")
    school = cursor.fetchone()
    if not school:
        print("NANJATI CDSS not found")
        return
    
    school_id = school[0]
    financial_year = '2026-2027'
    
    print(f"Cleaning POWs for school_id={school_id}, financial_year={financial_year}")
    
    # Get all unique codes
    cursor.execute('''SELECT DISTINCT code FROM budget_items 
                      WHERE school_id = ? AND financial_year = ?''',
                   (school_id, financial_year))
    codes = [row[0] for row in cursor.fetchall()]
    
    print(f"Found {len(codes)} unique POW codes")
    
    # For each code, keep only the first record and delete the rest
    for code in codes:
        cursor.execute('''SELECT id FROM budget_items 
                          WHERE school_id = ? AND financial_year = ? AND code = ?
                          ORDER BY id ASC''',
                       (school_id, financial_year, code))
        ids = [row[0] for row in cursor.fetchall()]
        
        if len(ids) > 1:
            keep_id = ids[0]
            delete_ids = ids[1:]
            print(f"Code {code}: Keeping id={keep_id}, deleting {len(delete_ids)} duplicates")
            
            for del_id in delete_ids:
                cursor.execute('DELETE FROM budget_items WHERE id = ?', (del_id,))
    
    conn.commit()
    
    # Verify final count
    cursor.execute('''SELECT COUNT(*) FROM budget_items 
                      WHERE school_id = ? AND financial_year = ?''',
                   (school_id, financial_year))
    final_count = cursor.fetchone()[0]
    print(f"\nFinal POW count: {final_count}")
    
    conn.close()

if __name__ == '__main__':
    clean_nanjati_pows()
