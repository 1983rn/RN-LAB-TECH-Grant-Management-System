#!/usr/bin/env python3
"""
Grant Management System - Multi-Tenant Application
"""
import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_cors import CORS
from datetime import datetime, timedelta

# Import multi-tenant modules
from database import init_database, get_db, log_action, generate_otp, hash_password
from auth import login_school, login_developer, require_login, require_developer, get_current_school_id

app = Flask(__name__)
CORS(app)
app.secret_key = os.urandom(24)

# Initialize database on startup
with app.app_context():
    if not os.path.exists('data/grant_management.db'):
        print("🔄 Initializing multi-tenant database...")
        init_database()
        from database import create_developer_account
        create_developer_account()
        print("✅ Database initialized")

@app.route('/')
def index():
    """Root route - redirect to login or dashboard"""
    if 'user' in session:
        if session['user'].get('is_developer'):
            return redirect(url_for('dev_dashboard'))
        return redirect(url_for('grant_summary'))
    return redirect(url_for('login_page'))

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """Login page and authentication"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        dev_mode = request.form.get('dev_mode') == '1'
        
        if dev_mode:
            # Developer login
            user, error = login_developer(username, password)
            if error:
                return render_template('login.html', error=error)
            session['user'] = user
            return redirect(url_for('dev_dashboard'))
        else:
            # School login
            user, error = login_school(username, password)
            if error:
                return render_template('login.html', error=error)
            session['user'] = user
            return redirect(url_for('grant_summary'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout and clear session"""
    if 'user' in session:
        school_id = get_current_school_id()
        if school_id:
            # Mark session as offline
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE school_sessions 
                    SET is_online = 0 
                    WHERE school_id = ? AND is_online = 1
                ''', (school_id,))
        session.pop('user', None)
    return redirect(url_for('login_page'))

# Developer Dashboard Routes
@app.route('/dev/dashboard')
@require_developer
def dev_dashboard():
    """Developer dashboard"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Get all schools (exclude developer account)
        cursor.execute('''
            SELECT id, school_name, username, is_active, is_locked, 
                   subscription_status, subscription_end, last_login
            FROM schools 
            WHERE school_name != 'DEVELOPER_ACCOUNT'
            ORDER BY school_name
        ''')
        schools = [dict(row) for row in cursor.fetchall()]
        
        # Get stats
        cursor.execute('SELECT COUNT(*) as total FROM schools WHERE school_name != "DEVELOPER_ACCOUNT"')
        total_schools = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as active FROM schools WHERE is_active = 1 AND school_name != "DEVELOPER_ACCOUNT"')
        active_schools = cursor.fetchone()['active']
        
        cursor.execute('''
            SELECT COUNT(DISTINCT school_id) as online 
            FROM school_sessions 
            WHERE is_online = 1 AND datetime(last_seen) > datetime('now', '-5 minutes')
        ''')
        online_schools = cursor.fetchone()['online']
        
        cursor.execute('SELECT COUNT(*) as expired FROM schools WHERE subscription_status = "EXPIRED"')
        expired_schools = cursor.fetchone()['expired']
        
        stats = {
            'total_schools': total_schools,
            'active_schools': active_schools,
            'online_schools': online_schools,
            'expired_schools': expired_schools
        }
    
    return render_template('developer_dashboard.html', schools=schools, stats=stats, session=session)

@app.route('/dev/add-school', methods=['POST'])
@require_developer
def dev_add_school():
    """Add new school"""
    school_name = request.form.get('school_name')
    username = request.form.get('username')
    password = request.form.get('password')
    subscription_end = request.form.get('subscription_end')
    
    with get_db() as conn:
        cursor = conn.cursor()
        password_hash = hash_password(password)
        
        try:
            cursor.execute('''
                INSERT INTO schools (school_name, username, password_hash, is_active, 
                                   subscription_status, subscription_end)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (school_name, username, password_hash, 1, 'PAID', subscription_end))
            
            school_id = cursor.lastrowid
            log_action('DEVELOPER', session['user']['username'], f'ADD_SCHOOL: {school_name}', 
                      school_id, request.remote_addr)
            
            return redirect(url_for('dev_dashboard'))
        except Exception as e:
            return render_template('developer_dashboard.html', error=str(e))

@app.route('/dev/reset-password/<int:school_id>', methods=['POST'])
@require_developer
def dev_reset_password(school_id):
    """Generate OTP for school"""
    otp = generate_otp()
    expires_at = datetime.now() + timedelta(hours=24)
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO password_reset_tokens (school_id, otp_code, expires_at)
            VALUES (?, ?, ?)
        ''', (school_id, otp, expires_at))
        
        log_action('DEVELOPER', session['user']['username'], f'RESET_PASSWORD', 
                  school_id, request.remote_addr)
    
    return jsonify({'success': True, 'otp': otp})

@app.route('/dev/lock-school/<int:school_id>', methods=['POST'])
@require_developer
def dev_lock_school(school_id):
    """Lock school account"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE schools SET is_locked = 1 WHERE id = ?', (school_id,))
        log_action('DEVELOPER', session['user']['username'], 'LOCK_SCHOOL', 
                  school_id, request.remote_addr)
    return jsonify({'success': True})

@app.route('/dev/unlock-school/<int:school_id>', methods=['POST'])
@require_developer
def dev_unlock_school(school_id):
    """Unlock school account"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE schools SET is_locked = 0 WHERE id = ?', (school_id,))
        log_action('DEVELOPER', session['user']['username'], 'UNLOCK_SCHOOL', 
                  school_id, request.remote_addr)
    return jsonify({'success': True})

@app.route('/dev/send-message/<int:school_id>', methods=['POST'])
@require_developer
def dev_send_message(school_id):
    """Send message to school"""
    data = request.get_json()
    message = data.get('message')
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO subscription_messages (school_id, message, message_type)
            VALUES (?, ?, ?)
        ''', (school_id, message, 'INFO'))
        
        log_action('DEVELOPER', session['user']['username'], 'SEND_MESSAGE', 
                  school_id, request.remote_addr)
    
    return jsonify({'success': True})

@app.route('/dev/send-expiry-warnings', methods=['POST'])
@require_developer
def dev_send_expiry_warnings():
    """Send warnings to schools expiring within 7 days"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, school_name FROM schools 
            WHERE subscription_end <= date('now', '+7 days')
            AND subscription_status != 'EXPIRED'
        ''')
        schools = cursor.fetchall()
        
        count = 0
        for school in schools:
            cursor.execute('''
                INSERT INTO subscription_messages (school_id, message, message_type)
                VALUES (?, ?, ?)
            ''', (school['id'], 
                  f'Your subscription expires soon. Please renew to continue access.',
                  'WARNING'))
            count += 1
    
    return jsonify({'success': True, 'count': count})

# Placeholder for school routes (to be integrated with existing app.py)
@app.route('/grant-summary')
@require_login
def grant_summary():
    """Grant summary dashboard - placeholder"""
    return f"<h1>Welcome {session['user']['name']}</h1><p>School Dashboard Coming Soon</p><a href='/logout'>Logout</a>"

if __name__ == '__main__':
    print("🚀 Starting Grant Management System - Multi-Tenant")
    print("📱 Access at: http://localhost:5176")
    print("\n🔐 Login Credentials:")
    print("   School: admin / admin123")
    print("   Developer: Type 'devaccess' on login screen")
    app.run(debug=True, host='0.0.0.0', port=5176)
