#!/usr/bin/env python3
"""
Grant Management System - Python Web Application
Fixed version with better error handling
"""

import json
import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = 'your-secret-key-here'

# Data storage (using JSON files instead of database for simplicity)
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)

def load_json_file(filename):
    """Load data from JSON file"""
    try:
        filepath = os.path.join(DATA_DIR, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return []

def save_json_file(filename, data):
    """Save data to JSON file"""
    try:
        filepath = os.path.join(DATA_DIR, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        return True
    except Exception as e:
        print(f"Error saving {filename}: {e}")
        return False

def get_budget(financial_year):
    """Get budget for specific financial year"""
    try:
        budgets = load_json_file('budgets.json')
        for budget in budgets:
            if budget.get('financialYear') == financial_year:
                return budget
        return None
    except Exception as e:
        print(f"Error getting budget: {e}")
        return None

def save_budget(budget_data):
    """Save budget data"""
    try:
        budgets = load_json_file('budgets.json')
        # Remove existing budget for same year
        budgets = [b for b in budgets if b.get('financialYear') != budget_data['financialYear']]
        budgets.append(budget_data)
        return save_json_file('budgets.json', budgets)
    except Exception as e:
        print(f"Error saving budget: {e}")
        return False

def get_credits(financial_year):
    """Get credits for specific financial year"""
    try:
        credits = load_json_file('credits.json')
        return [c for c in credits if c.get('financialYear') == financial_year]
    except Exception as e:
        print(f"Error getting credits: {e}")
        return []

def save_credit(credit_data):
    """Save credit data"""
    try:
        credits = load_json_file('credits.json')
        credits.append(credit_data)
        return save_json_file('credits.json', credits)
    except Exception as e:
        print(f"Error saving credit: {e}")
        return False

def get_debits(financial_year):
    """Get debits for specific financial year"""
    try:
        debits = load_json_file('debits.json')
        if isinstance(debits, list):
            return [d for d in debits if d.get('financialYear') == financial_year]
        else:
            return []
    except Exception as e:
        print(f"Error getting debits: {e}")
        return []

def save_debit(debit_data):
    """Save debit data"""
    try:
        debits = load_json_file('debits.json')
        debits.append(debit_data)
        return save_json_file('debits.json', debits)
    except Exception as e:
        print(f"Error saving debit: {e}")
        return False

def calculate_spending(budget, debits):
    """Calculate spending for budget items"""
    try:
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
    except Exception as e:
        print(f"Error calculating spending: {e}")
        return []

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
    try:
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
    except Exception as e:
        print(f"Error in index route: {e}")
        return f"Error: {e}", 500

@app.route('/budget')
def budget():
    """Budget allocation page"""
    try:
        financial_year = request.args.get('financial_year', '2026-2027')
        budget = get_budget(financial_year)
        
        return render_template('budget.html',
                          budget=budget,
                          financial_year=financial_year,
                          current_page='budget')
    except Exception as e:
        print(f"Error in budget route: {e}")
        return f"Error: {e}", 500

@app.route('/initialize_budget', methods=['GET', 'POST'])
def initialize_budget():
    """Initialize budget"""
    try:
        if request.method == 'POST':
            print("Received POST request to initialize_budget")
            data = request.get_json()
            print(f"Data received: {data}")
            
            budget_data = {
                'financialYear': data.get('financialYear'),
                'schoolName': data.get('schoolName'),
                'totalGrant': data.get('totalGrant'),
                'items': generate_budget_structure(),
                'createdAt': datetime.now().isoformat()
            }
            
            if save_budget(budget_data):
                print("Budget saved successfully")
                return jsonify({'success': True, 'budget': budget_data})
            else:
                print("Failed to save budget")
                return jsonify({'success': False, 'error': 'Failed to save budget'})
        
        return render_template('initialize_budget.html')
    except Exception as e:
        print(f"Error in initialize_budget route: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/credits')
def credits():
    """Credit register page"""
    try:
        financial_year = request.args.get('financial_year', '2026-2027')
        budget = get_budget(financial_year)
        credits = get_credits(financial_year)
        
        return render_template('credits.html',
                          budget=budget,
                          credits=credits,
                          financial_year=financial_year,
                          current_page='credits')
    except Exception as e:
        print(f"Error in credits route: {e}")
        return f"Error: {e}", 500

@app.route('/add_credit', methods=['POST'])
def add_credit():
    """Add credit entry"""
    try:
        print("Received POST request to add_credit")
        data = request.get_json()
        print(f"Credit data received: {data}")
        
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
            print("Credit saved successfully")
            return jsonify({'success': True, 'credit': credit_data})
        else:
            print("Failed to save credit")
            return jsonify({'success': False, 'error': 'Failed to save credit'})
    except Exception as e:
        print(f"Error in add_credit route: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/debits')
def debits():
    """Debit register page"""
    try:
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
    except Exception as e:
        print(f"Error in debits route: {e}")
        return render_template('error.html', error=str(e)), 500

@app.route('/add_debit', methods=['POST'])
def add_debit():
    """Add debit entry"""
    try:
        print("Received POST request to add_debit")
        data = request.get_json()
        print(f"Debit data received: {data}")
        
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
            print("Debit saved successfully")
            return jsonify({'success': True, 'debit': debit_data})
        else:
            print("Failed to save debit")
            return jsonify({'success': False, 'error': 'Failed to save debit'})
    except Exception as e:
        print(f"Error in add_debit route: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/tracking')
def tracking():
    """Spending tracking page"""
    try:
        financial_year = request.args.get('financial_year', '2026-2027')
        budget = get_budget(financial_year)
        debits = get_debits(financial_year)
        spending = calculate_spending(budget, debits)
        
        return render_template('tracking.html',
                          budget=budget,
                          spending=spending,
                          financial_year=financial_year,
                          current_page='tracking')
    except Exception as e:
        print(f"Error in tracking route: {e}")
        return f"Error: {e}", 500

@app.route('/clear_registers', methods=['POST'])
def clear_registers():
    """Clear all registers"""
    try:
        data = request.get_json()
        financial_year = data.get('financialYear')
        
        # Clear credits and debits for the financial year
        credits = load_json_file('credits.json')
        debits = load_json_file('debits.json')
        
        credits = [c for c in credits if c.get('financialYear') != financial_year]
        debits = [d for d in debits if d.get('financialYear') != financial_year]
        
        save_json_file('credits.json', credits)
        save_json_file('debits.json', debits)
        
        return jsonify({'success': True, 'message': 'All registers cleared successfully'})
    except Exception as e:
        print(f"Error clearing registers: {e}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print("🚀 Starting Grant Management System (Python - Fixed Version)")
    print("📱 Access at: http://localhost:5175")
    app.run(debug=True, host='0.0.0.0', port=5175)
