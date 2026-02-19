#!/usr/bin/env python3
"""
Test Suite for Grant Management System - Python Version
"""

import unittest
import json
import tempfile
import os
from app import app

class GrantManagementTestCase(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = app.test_client()
        self.app.testing = True
        
        # Create temporary data directory
        self.temp_dir = tempfile.mkdtemp()
        app.config['DATA_DIR'] = self.temp_dir
        
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_index_page(self):
        """Test that the index page loads"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Grant Management System', response.data)
    
    def test_budget_page(self):
        """Test that the budget page loads"""
        response = self.app.get('/budget')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Budget Allocation', response.data)
    
    def test_credits_page(self):
        """Test that the credits page loads"""
        response = self.app.get('/credits')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Credit Register', response.data)
    
    def test_debits_page(self):
        """Test that the debits page loads"""
        response = self.app.get('/debits')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Debit Register', response.data)
    
    def test_tracking_page(self):
        """Test that the tracking page loads"""
        response = self.app.get('/tracking')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Spending Tracking', response.data)
    
    def test_initialize_budget(self):
        """Test budget initialization"""
        budget_data = {
            'financialYear': '2026-2027',
            'schoolName': 'Test School',
            'totalGrant': 100000
        }
        
        response = self.app.post('/initialize_budget',
                               data=json.dumps(budget_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('budget', data)
    
    def test_add_credit(self):
        """Test adding a credit entry"""
        # First initialize a budget
        budget_data = {
            'financialYear': '2026-2027',
            'schoolName': 'Test School',
            'totalGrant': 100000
        }
        self.app.post('/initialize_budget',
                     data=json.dumps(budget_data),
                     content_type='application/json')
        
        # Add credit
        credit_data = {
            'date': '2026-01-15',
            'month': 'January',
            'lineItems': [
                {'subItemDescription': 'Test Item', 'amount': 1000}
            ],
            'remarks': 'Test credit',
            'financialYear': '2026-2027'
        }
        
        response = self.app.post('/add_credit',
                               data=json.dumps(credit_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('credit', data)
    
    def test_add_debit(self):
        """Test adding a debit entry"""
        # First initialize a budget
        budget_data = {
            'financialYear': '2026-2027',
            'schoolName': 'Test School',
            'totalGrant': 100000
        }
        self.app.post('/initialize_budget',
                     data=json.dumps(budget_data),
                     content_type='application/json')
        
        # Add debit
        debit_data = {
            'date': '2026-01-15',
            'month': 'January',
            'itemId': 'pow1',
            'subItemDescription': 'Test Item',
            'code': 'TEST001',
            'description': 'Test debit',
            'amount': 500,
            'supplierName': 'Test Supplier',
            'position': 'Bursar',
            'financialYear': '2026-2027'
        }
        
        response = self.app.post('/add_debit',
                               data=json.dumps(debit_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('debit', data)
    
    def test_clear_registers(self):
        """Test clearing all registers"""
        # First add some data
        budget_data = {
            'financialYear': '2026-2027',
            'schoolName': 'Test School',
            'totalGrant': 100000
        }
        self.app.post('/initialize_budget',
                     data=json.dumps(budget_data),
                     content_type='application/json')
        
        credit_data = {
            'date': '2026-01-15',
            'month': 'January',
            'lineItems': [{'subItemDescription': 'Test', 'amount': 1000}],
            'remarks': 'Test',
            'financialYear': '2026-2027'
        }
        self.app.post('/add_credit',
                     data=json.dumps(credit_data),
                     content_type='application/json')
        
        # Clear registers
        response = self.app.post('/clear_registers',
                               data=json.dumps({'financialYear': '2026-2027'}),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
    
    def test_invalid_json_request(self):
        """Test handling of invalid JSON requests"""
        response = self.app.post('/initialize_budget',
                               data='invalid json',
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
    
    def test_missing_required_fields(self):
        """Test handling of missing required fields"""
        budget_data = {
            'financialYear': '2026-2027'
            # Missing schoolName and totalGrant
        }
        
        response = self.app.post('/initialize_budget',
                               data=json.dumps(budget_data),
                               content_type='application/json')
        
        # Should handle missing fields gracefully
        self.assertIn(response.status_code, [200, 400])

if __name__ == '__main__':
    unittest.main()
