import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import generate_budget_structure
import sqlite3
import json

conn = sqlite3.connect('data/grant_management.db')
cursor = conn.cursor()

items = generate_budget_structure()
for item in items:
    cursor.execute('''INSERT INTO budget_items 
        (school_id, financial_year, item_key, pow_no, pow_name, sub_activity, 
         sub_item_description, code, total_allocation, monthly_allocations) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (1, '2026-2027', item['id'], item['powNo'], item['powName'], 
         item['subActivity'], item['subItemDescription'], item['code'], 
         0, json.dumps(item['monthlyAllocations'])))

conn.commit()
cursor.execute('SELECT COUNT(*) FROM budget_items WHERE school_id = 1')
print(f'Total POWs: {cursor.fetchone()[0]}')
conn.close()
