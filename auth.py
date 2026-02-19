"""
Authentication and Session Management
"""
from flask import session, redirect, url_for, request
from functools import wraps
from database import get_db, hash_password, verify_password, log_action
from datetime import datetime

def login_school(username, password):
    """Authenticate school user"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, school_name, password_hash, is_active, is_locked, 
                   subscription_status, subscription_end
            FROM schools WHERE username = ?
        ''', (username,))
        school = cursor.fetchone()
        
        if not school:
            return None, "Invalid credentials"
        
        if not verify_password(password, school['password_hash']):
            return None, "Invalid credentials"
        
        if school['is_locked']:
            return None, "Account locked. Contact administrator."
        
        if not school['is_active']:
            return None, "Account inactive"
        
        # Check subscription status
        if school['subscription_end']:
            expiry_date = datetime.strptime(school['subscription_end'], '%Y-%m-%d')
            if expiry_date < datetime.now():
                # Update status to expired
                cursor.execute('UPDATE schools SET subscription_status = ? WHERE id = ?', 
                              ('EXPIRED', school['id']))
                if school['subscription_status'] == 'TRIAL':
                    return None, "Trial period expired. Please contact developer for subscription."
                else:
                    return None, "Subscription expired. Please renew your subscription."
        
        # Update last login
        cursor.execute('UPDATE schools SET last_login = ? WHERE id = ?', 
                      (datetime.now(), school['id']))
        
        # Create session
        cursor.execute('''
            INSERT INTO school_sessions (school_id, login_time, last_seen, is_online)
            VALUES (?, ?, ?, ?)
        ''', (school['id'], datetime.now(), datetime.now(), 1))
    
    # Store school name and financial year in session
    session['school_name'] = school['school_name']
    session['school_id'] = school['id']
    
    # Log action outside transaction - don't fail login if logging fails
    log_action('SCHOOL', str(school['id']), 'LOGIN', school['id'], request.remote_addr)
    
    return {
        'id': school['id'],
        'name': school['school_name'],
        'username': username,
        'is_developer': username == 'juniornsambe@yahoo.com'
    }, None

def login_developer(username, password):
    """Authenticate developer"""
    # Trim whitespace from inputs
    username = username.strip() if username else ''
    password = password.strip() if password else ''
    
    print(f"[DEBUG] Developer login attempt: username='{username}', password_len={len(password)}")
    
    if username != 'juniornsambe@yahoo.com':
        print(f"[DEBUG] Username mismatch: expected 'juniornsambe@yahoo.com', got '{username}'")
        return None, "Invalid developer credentials"
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, password_hash, is_active, is_locked FROM schools 
            WHERE username = ? AND school_name = 'DEVELOPER_ACCOUNT'
        ''', (username,))
        dev = cursor.fetchone()
        
        if not dev:
            print("[DEBUG] Developer account not found in database")
            return None, "Invalid developer credentials"
        
        print(f"[DEBUG] Developer account found: id={dev['id']}, active={dev['is_active']}, locked={dev['is_locked']}")
        
        if not verify_password(password, dev['password_hash']):
            print("[DEBUG] Password verification failed")
            return None, "Invalid developer credentials"
        
        print("[DEBUG] Developer login successful")
    
    # Log action outside transaction - don't fail login if logging fails
    log_action('DEVELOPER', username, 'LOGIN', None, request.remote_addr)
    
    return {
        'id': dev['id'],
        'name': 'Developer',
        'username': username,
        'is_developer': True
    }, None

def require_login(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

def require_developer(f):
    """Decorator to require developer access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or not session['user'].get('is_developer'):
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_school_id():
    """Get current logged-in school ID"""
    if 'user' in session and not session['user'].get('is_developer'):
        return session['user']['id']
    return None

def update_last_seen():
    """Update last seen timestamp for online tracking"""
    school_id = get_current_school_id()
    if school_id:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE school_sessions 
                SET last_seen = ?, is_online = 1
                WHERE school_id = ? AND is_online = 1
            ''', (datetime.now(), school_id))
