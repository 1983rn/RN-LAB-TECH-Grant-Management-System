import requests
import json

# Test the initialize_budget endpoint
url = "http://localhost:5173/initialize_budget"
data = {
    "financialYear": "2026-2027",
    "schoolName": "Test School",
    "totalGrant": 100000
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
