#!/usr/bin/env python3
"""
Grant Management System - Python Web Application
Converted from React/TypeScript to Python Flask
"""

import json
import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = 'your-secret-key-here'

# Data storage (using JSON files instead of database for simplicity)
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)

def load_data(filename):
    """Load data from JSON file"""
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return []

def save_data(filename, data):
    """Save data to JSON file"""
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, default=str)

def get_budget(financial_year):
    """Get budget for specific financial year"""
    budgets = load_data('budgets.json')
    for budget in budgets:
        if budget.get('financialYear') == financial_year:
            return budget
    return None

def save_budget(budget_data):
    """Save budget data"""
    budgets = load_data('budgets.json')
    # Remove existing budget for same year
    budgets = [b for b in budgets if b.get('financialYear') != budget_data['financialYear']]
    budgets.append(budget_data)
    save_data('budgets.json', budgets)

def get_credits(financial_year):
    """Get credits for specific financial year"""
    credits = load_data('credits.json')
    return [c for c in credits if c.get('financialYear') == financial_year]

def save_credit(credit_data):
    """Save credit data"""
    credits = load_data('credits.json')
    credits.append(credit_data)
    save_data('credits.json', credits)

def update_credit(index, credit_data):
    """Update credit data"""
    credits = load_data('credits.json')
    if 0 <= index < len(credits):
        credits[index] = credit_data
        save_data('credits.json', credits)

def delete_credit(index):
    """Delete credit data"""
    credits = load_data('credits.json')
    if 0 <= index < len(credits):
        credits.pop(index)
        save_data('credits.json', credits)

def get_debits(financial_year):
    """Get debits for specific financial year"""
    debits = load_data('debits.json')
    return [d for d in debits if d.get('financialYear') == financial_year]

def save_debit(debit_data):
    """Save debit data"""
    debits = load_data('debits.json')
    debits.append(debit_data)
    save_data('debits.json', debits)

def update_debit(index, debit_data):
    """Update debit data"""
    debits = load_data('debits.json')
    if 0 <= index < len(debits):
        debits[index] = debit_data
        save_data('debits.json', debits)

def delete_debit(index):
    """Delete debit data"""
    debits = load_data('debits.json')
    if 0 <= index < len(debits):
        debits.pop(index)
        save_data('debits.json', debits)

def calculate_spending(budget, debits):
    """Calculate spending for budget items"""
    if not budget:
        return []
    
    items = []
    for budget_item in budget.get('items', []):
        item_debits = [d for d in debits if d.get('itemId') == budget_item.get('id')]
        spent = sum(d.get('amount', 0) for d in item_debits)
        
        items.append({
            'id': budget_item.get('id'),
            'powName': budget_item.get('powName'),
            'subActivity': budget_item.get('subActivity'),
            'subItemDescription': budget_item.get('subItemDescription'),
            'totalAllocation': budget_item.get('totalAllocation', 0),
            'spent': spent,
            'balance': budget_item.get('totalAllocation', 0) - spent
        })
    
    return items

# Routes
@app.route('/')
def index():
    """Main dashboard"""
    financial_year = request.args.get('financial_year', '2026-2027')
    budget = get_budget(financial_year)
    credits = get_credits(financial_year)
    debits = get_debits(financial_year)
    spending = calculate_spending(budget, debits)
    
    return render_template('index.html', 
                      budget=budget,
                      credits=credits,
                      debits=debits,
                      spending=spending,
                      financial_year=financial_year,
                      current_page='dashboard')

@app.route('/budget')
def budget():
    """Budget allocation page"""
    financial_year = request.args.get('financial_year', '2026-2027')
    budget = get_budget(financial_year)
    
    return render_template('budget.html',
                      budget=budget,
                      financial_year=financial_year,
                      current_page='budget')

@app.route('/initialize_budget', methods=['GET', 'POST'])
def initialize_budget():
    """Initialize budget"""
    if request.method == 'POST':
        data = request.get_json()
        budget_data = {
            'financialYear': data.get('financialYear'),
            'schoolName': data.get('schoolName'),
            'totalGrant': data.get('totalGrant'),
            'items': generate_budget_structure(),
            'createdAt': datetime.now().isoformat()
        }
        save_budget(budget_data)
        return jsonify({'success': True, 'budget': budget_data})
    
    return render_template('initialize_budget.html')

@app.route('/update_budget', methods=['POST'])
def update_budget():
    """Update budget"""
    data = request.get_json()
    financial_year = data.get('financialYear')
    budget = get_budget(financial_year)
    
    if budget:
        budget.update(data)
        budget['updatedAt'] = datetime.now().isoformat()
        save_budget(budget)
        return jsonify({'success': True, 'budget': budget})
    
    return jsonify({'success': False, 'error': 'Budget not found'})

@app.route('/credits')
def credits():
    """Credit register page"""
    financial_year = request.args.get('financial_year', '2026-2027')
    budget = get_budget(financial_year)
    credits = get_credits(financial_year)
    
    return render_template('credits.html',
                      budget=budget,
                      credits=credits,
                      financial_year=financial_year,
                      current_page='credits')

@app.route('/add_credit', methods=['POST'])
def add_credit():
    """Add credit entry"""
    data = request.get_json()
    credit_data = {
        'id': f"credit_{datetime.now().timestamp()}",
        'date': data.get('date'),
        'month': data.get('month'),
        'lineItems': data.get('lineItems', []),
        'remarks': data.get('remarks'),
        'financialYear': data.get('financialYear'),
        'createdAt': datetime.now().isoformat()
    }
    save_credit(credit_data)
    return jsonify({'success': True, 'credit': credit_data})

@app.route('/update_credit/<int:index>', methods=['POST'])
def update_credit_route(index):
    """Update credit entry"""
    data = request.get_json()
    financial_year = data.get('financialYear')
    credits = get_credits(financial_year)
    
    if 0 <= index < len(credits):
        credits[index].update(data)
        credits[index]['updatedAt'] = datetime.now().isoformat()
        
        # Save all credits
        all_credits = load_data('credits.json')
        for i, credit in enumerate(all_credits):
            if credit.get('financialYear') == financial_year and i < len(credits):
                all_credits[i] = credits[i]
        save_data('credits.json', all_credits)
        
        return jsonify({'success': True})
    
    return jsonify({'success': False, 'error': 'Credit not found'})

@app.route('/delete_credit/<int:index>', methods=['POST'])
def delete_credit_route(index):
    """Delete credit entry"""
    financial_year = request.form.get('financial_year', '2026-2027')
    delete_credit(index)
    return redirect(url_for('credits', financial_year=financial_year))

@app.route('/debits')
def debits():
    """Debit register page"""
    financial_year = request.args.get('financial_year', '2026-2027')
    budget = get_budget(financial_year)
    credits = get_credits(financial_year)
    debits = get_debits(financial_year)
    
    return render_template('debits.html',
                      budget=budget,
                      credits=credits,
                      debits=debits,
                      financial_year=financial_year,
                      current_page='debits')

@app.route('/add_debit', methods=['POST'])
def add_debit():
    """Add debit entry"""
    data = request.get_json()
    debit_data = {
        'id': f"debit_{datetime.now().timestamp()}",
        'date': data.get('date'),
        'month': data.get('month'),
        'itemId': data.get('itemId'),
        'subItemDescription': data.get('subItemDescription'),
        'code': data.get('code'),
        'description': data.get('description'),
        'amount': data.get('amount'),
        'supplierName': data.get('supplierName'),
        'position': data.get('position'),
        'financialYear': data.get('financialYear'),
        'createdAt': datetime.now().isoformat()
    }
    save_debit(debit_data)
    return jsonify({'success': True, 'debit': debit_data})

@app.route('/update_debit/<int:index>', methods=['POST'])
def update_debit_route(index):
    """Update debit entry"""
    data = request.get_json()
    financial_year = data.get('financialYear')
    debits = get_debits(financial_year)
    
    if 0 <= index < len(debits):
        debits[index].update(data)
        debits[index]['updatedAt'] = datetime.now().isoformat()
        
        # Save all debits
        all_debits = load_data('debits.json')
        for i, debit in enumerate(all_debits):
            if debit.get('financialYear') == financial_year and i < len(debits):
                all_debits[i] = debits[i]
        save_data('debits.json', all_debits)
        
        return jsonify({'success': True})
    
    return jsonify({'success': False, 'error': 'Debit not found'})

@app.route('/delete_debit/<int:index>', methods=['POST'])
def delete_debit_route(index):
    """Delete debit entry"""
    financial_year = request.form.get('financial_year', '2026-2027')
    delete_debit(index)
    return redirect(url_for('debits', financial_year=financial_year))

@app.route('/tracking')
def tracking():
    """Spending tracking page"""
    financial_year = request.args.get('financial_year', '2026-2027')
    budget = get_budget(financial_year)
    debits = get_debits(financial_year)
    spending = calculate_spending(budget, debits)
    
    return render_template('tracking.html',
                      budget=budget,
                      spending=spending,
                      financial_year=financial_year,
                      current_page='tracking')

@app.route('/clear_registers', methods=['POST'])
def clear_registers():
    """Clear all registers"""
    data = request.get_json()
    financial_year = data.get('financialYear')
    
    # Clear credits and debits for the financial year
    credits = load_data('credits.json')
    debits = load_data('debits.json')
    
    credits = [c for c in credits if c.get('financialYear') != financial_year]
    debits = [d for d in debits if d.get('financialYear') != financial_year]
    
    save_data('credits.json', credits)
    save_data('debits.json', debits)
    
    return jsonify({'success': True, 'message': 'All registers cleared successfully'})

def generate_budget_structure():
    """Generate default budget structure"""
    return [
        {
            'id': 'pow1',
            'powName': 'Teaching and Learning Materials',
            'subActivity': 'Classroom Supplies',
            'subItemDescription': 'Exercise Books',
            'code': 'TLM001',
            'totalAllocation': 0
        },
        {
            'id': 'pow2',
            'powName': 'Teaching and Learning Materials',
            'subActivity': 'Classroom Supplies',
            'subItemDescription': 'Textbooks',
            'code': 'TLM002',
            'totalAllocation': 0
        },
        {
            'id': 'pow3',
            'powName': 'School Operations',
            'subActivity': 'Maintenance',
            'subItemDescription': 'Building Repairs',
            'code': 'SO001',
            'totalAllocation': 0
        }
    ]

if __name__ == '__main__':
    print("🚀 Starting Grant Management System (Python)")
    print("📱 Access at: http://localhost:5173")
    app.run(debug=True, host='0.0.0.0', port=5173)
