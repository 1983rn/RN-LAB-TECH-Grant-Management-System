#!/usr/bin/env python3
"""
Debug script to test debits function
"""

import json
import os

# Test the load_data function directly
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)

def load_data(filename):
    """Load data from JSON file"""
    filepath = os.path.join(DATA_DIR, filename)
    print(f"Loading from: {filepath}")
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            data = json.load(f)
            print(f"Loaded data type: {type(data)}")
            print(f"Loaded data: {data}")
            return data
    print("File doesn't exist, returning []")
    return []

def get_debits(financial_year):
    """Get debits for specific financial year"""
    try:
        debits = load_data('debits.json')
        print(f"Debits type: {type(debits)}")
        print(f"Debits value: {debits}")
        
        if isinstance(debits, list):
            result = [d for d in debits if d.get('financialYear') == financial_year]
            print(f"Result type: {type(result)}")
            print(f"Result value: {result}")
            return result
        else:
            print("Debits is not a list!")
            return []
    except Exception as e:
        print(f"Error getting debits: {e}")
        return []

# Test the functions
if __name__ == '__main__':
    print("Testing debits function...")
    debits = get_debits('2026-2027')
    print(f"Final result: {debits}")
    print(f"Final result type: {type(debits)}")
