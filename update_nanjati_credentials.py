"""
Update NANJATI CDSS login credentials
Username: NANJATICDSS
Password: 1994
"""
from database import get_db, hash_password

def update_nanjati_credentials():
    """Update NANJATI CDSS credentials"""
    new_username = 'NANJATICDSS'
    new_password = '1994'
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Find NANJATI CDSS account (username 'admin' or school_name contains 'NANJATI')
        cursor.execute("""
            SELECT id, school_name, username FROM schools 
            WHERE username = 'admin' OR school_name LIKE '%NANJATI%'
            LIMIT 1
        """)
        school = cursor.fetchone()
        
        if school:
            school_id = school['id']
            old_username = school['username']
            
            # Hash the new password
            password_hash = hash_password(new_password)
            
            # Update credentials
            cursor.execute("""
                UPDATE schools 
                SET username = ?, password_hash = ?
                WHERE id = ?
            """, (new_username, password_hash, school_id))
            
            print("[SUCCESS] Updated NANJATI CDSS credentials:")
            print(f"   Old username: {old_username}")
            print(f"   New username: {new_username}")
            print(f"   New password: {new_password}")
            print(f"\n[SUCCESS] Login with: {new_username} / {new_password}")
        else:
            print("[ERROR] NANJATI CDSS account not found")

if __name__ == '__main__':
    update_nanjati_credentials()
