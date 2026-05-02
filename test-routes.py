#!/usr/bin/env python3
"""
Test all routes in the Flask app
"""

import requests

def test_routes():
    base_url = 'http://localhost:5176'
    
    print('🔍 Testing all Flask routes')
    print('=' * 50)
    
    # Test all possible routes
    routes = [
        ('/', 'GET'),
        ('/budget', 'GET'),
        ('/initialize_budget', 'GET'),
        ('/initialize_budget', 'POST'),
        ('/update_budget', 'POST'),
        ('/credits', 'GET'),
        ('/add_credit', 'POST'),
        ('/debits', 'GET'),
        ('/add_debit', 'POST'),
        ('/tracking', 'GET'),
        ('/clear_registers', 'POST')
    ]
    
    for route, method in routes:
        try:
            if method == 'GET':
                response = requests.get(f'{base_url}{route}')
            else:
                response = requests.post(f'{base_url}{route}', json={'test': 'data'})
            
            status = '✅' if response.status_code == 200 else '❌'
            print(f'{status} {method} {route}: {response.status_code}')
            
            if response.status_code != 200:
                print(f'   Response: {response.text[:200]}')
        except Exception as e:
            print(f'❌ {method} {route}: ERROR - {e}')
    
    print('=' * 50)
    print('🎉 ROUTE TEST COMPLETE')

if __name__ == '__main__':
    test_routes()
