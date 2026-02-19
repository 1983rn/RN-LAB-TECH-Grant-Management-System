#!/usr/bin/env python3
"""
Minimal Flask app to test without conflicts
"""

import json
import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Use different function name to avoid conflicts
def load_json_data(filename):
    """Load data from JSON file"""
    filepath = os.path.join('data', filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return []

def get_debits_simple(financial_year):
    """Get debits for specific financial year"""
    debits = load_json_data('debits.json')
    return [d for d in debits if d.get('financialYear') == financial_year]

@app.route('/debits')
def debits():
    """Debit register page"""
    try:
        financial_year = request.args.get('financial_year', '2026-2027')
        debits = get_debits_simple(financial_year)
        
        return f"Debits page working! Found {len(debits)} debits"
    except Exception as e:
        return f"Error: {e}", 500

if __name__ == '__main__':
    print("🧪 Starting minimal Flask app on port 5176")
    app.run(debug=True, host='0.0.0.0', port=5176)
