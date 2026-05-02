#!/usr/bin/env python3
"""
Grant Management System - Python Web Application
Final working version
"""

import json
import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = 'your-secret-key-here'

# Data storage
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)

def read_json_file(filename):
    """Read JSON file"""
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def write_json_file(filename, data):
    """Write JSON file"""
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_budget(financial_year):
    """Get budget for specific financial year"""
    budgets = read_json_file('budgets.json')
    for budget in budgets:
        if budget.get('financialYear') == financial_year:
            return budget
    return None

def save_budget(budget_data):
    """Save budget data"""
    budgets = read_json_file('budgets.json')
    budgets = [b for b in budgets if b.get('financialYear') != budget_data['financialYear']]
    budgets.append(budget_data)
    write_json_file('budgets.json', budgets)
    return True

def get_credits(financial_year):
    """Get credits for specific financial year"""
    credits = read_json_file('credits.json')
    return [c for c in credits if c.get('financialYear') == financial_year]

def save_credit(credit_data):
    """Save credit data"""
    credits = read_json_file('credits.json')
    credits.append(credit_data)
    write_json_file('credits.json', credits)
    return True

def get_debits(financial_year):
    """Get debits for specific financial year"""
    debits = read_json_file('debits.json')
    return [d for d in debits if d.get('financialYear') == financial_year]

def save_debit(debit_data):
    """Save debit data"""
    debits = read_json_file('debits.json')
    debits.append(debit_data)
    write_json_file('debits.json', debits)
    return True

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
        
        if save_budget(budget_data):
            return jsonify({'success': True, 'budget': budget_data})
        else:
            return jsonify({'success': False, 'error': 'Failed to save budget'})
    
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
        
        if save_budget(budget):
            return jsonify({'success': True, 'budget': budget})
        else:
            return jsonify({'success': False, 'error': 'Failed to save budget'})
    
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
    
    if save_credit(credit_data):
        return jsonify({'success': True, 'credit': credit_data})
    else:
        return jsonify({'success': False, 'error': 'Failed to save credit'})

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
    
    if save_debit(debit_data):
        return jsonify({'success': True, 'debit': debit_data})
    else:
        return jsonify({'success': False, 'error': 'Failed to save debit'})

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
    credits = read_json_file('credits.json')
    debits = read_json_file('debits.json')
    
    credits = [c for c in credits if c.get('financialYear') != financial_year]
    debits = [d for d in debits if d.get('financialYear') != financial_year]
    
    write_json_file('credits.json', credits)
    write_json_file('debits.json', debits)
    
    return jsonify({'success': True, 'message': 'All registers cleared successfully'})

if __name__ == '__main__':
    print("🚀 Starting Grant Management System (Python - Final Version)")
    print("📱 Access at: http://localhost:5176")
    app.run(debug=True, host='0.0.0.0', port=5176)
