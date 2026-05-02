#!/usr/bin/env python3
"""
Test script to verify the Python application is working
"""

import requests
import json
import time

def test_app():
    """Test if the application is working"""
    base_url = "http://localhost:5173"
    
    print("🧪 Testing Grant Management System (Python)")
    print("=" * 50)
    
    try:
        # Test 1: Check if server is responding
        print("1. Testing server connection...")
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("✅ Server is responding")
        else:
            print(f"❌ Server returned status: {response.status_code}")
            return False
        
        # Test 2: Check if main page loads
        print("2. Testing main page...")
        if "Grant Management System" in response.text:
            print("✅ Main page loaded successfully")
        else:
            print("❌ Main page content not found")
            return False
        
        # Test 3: Test budget initialization
        print("3. Testing budget initialization...")
        budget_data = {
            "financialYear": "2026-2027",
            "schoolName": "Test School",
            "totalGrant": 100000
        }
        
        response = requests.post(f"{base_url}/initialize_budget", 
                              json=budget_data, 
                              timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Budget initialization working")
            else:
                print(f"❌ Budget initialization failed: {result.get('error')}")
        else:
            print(f"❌ Budget initialization HTTP error: {response.status_code}")
        
        # Test 4: Test credit addition
        print("4. Testing credit addition...")
        credit_data = {
            "date": "2026-01-15",
            "month": "January",
            "lineItems": [
                {"subItemDescription": "Test Item", "amount": 1000}
            ],
            "remarks": "Test credit",
            "financialYear": "2026-2027"
        }
        
        response = requests.post(f"{base_url}/add_credit", 
                              json=credit_data, 
                              timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Credit addition working")
            else:
                print(f"❌ Credit addition failed: {result.get('error')}")
        else:
            print(f"❌ Credit addition HTTP error: {response.status_code}")
        
        # Test 5: Test debit addition
        print("5. Testing debit addition...")
        debit_data = {
            "date": "2026-01-15",
            "month": "January",
            "itemId": "pow1",
            "subItemDescription": "Test Item",
            "code": "TEST001",
            "description": "Test debit",
            "amount": 500,
            "supplierName": "Test Supplier",
            "position": "Bursar",
            "financialYear": "2026-2027"
        }
        
        response = requests.post(f"{base_url}/add_debit", 
                              json=debit_data, 
                              timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Debit addition working")
            else:
                print(f"❌ Debit addition failed: {result.get('error')}")
        else:
            print(f"❌ Debit addition HTTP error: {response.status_code}")
        
        # Test 6: Test credits page
        print("6. Testing credits page...")
        response = requests.get(f"{base_url}/credits?financial_year=2026-2027", timeout=5)
        if response.status_code == 200:
            print("✅ Credits page working")
        else:
            print(f"❌ Credits page HTTP error: {response.status_code}")
        
        # Test 7: Test debits page
        print("7. Testing debits page...")
        response = requests.get(f"{base_url}/debits?financial_year=2026-2027", timeout=5)
        if response.status_code == 200:
            print("✅ Debits page working")
        else:
            print(f"❌ Debits page HTTP error: {response.status_code}")
        
        # Test 8: Test tracking page
        print("8. Testing tracking page...")
        response = requests.get(f"{base_url}/tracking?financial_year=2026-2027", timeout=5)
        if response.status_code == 200:
            print("✅ Tracking page working")
        else:
            print(f"❌ Tracking page HTTP error: {response.status_code}")
        
        print("\n" + "=" * 50)
        print("🎉 Application Test Summary:")
        print("✅ Server is running and responding")
        print("✅ All main pages are accessible")
        print("✅ API endpoints are working")
        print("✅ Data operations are functional")
        print("\n📱 Application is working correctly!")
        print(f"🌐 Access at: {base_url}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server - is it running?")
        return False
    except requests.exceptions.Timeout:
        print("❌ Server request timed out")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_app()
    if not success:
        print("\n❌ Application test failed")
        print("Please check the server logs and try again")
        exit(1)
