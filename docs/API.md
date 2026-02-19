# API Documentation

## Grant Management System - Python Flask API

### Base URL
```
http://localhost:5173
```

### Authentication
No authentication required for local development.

### Endpoints

#### Budget Management

##### Initialize Budget
```http
POST /initialize_budget
Content-Type: application/json

{
  "financialYear": "2026-2027",
  "schoolName": "Example School",
  "totalGrant": 100000
}
```

**Response:**
```json
{
  "success": true,
  "budget": {
    "financialYear": "2026-2027",
    "schoolName": "Example School",
    "totalGrant": 100000,
    "items": [...],
    "createdAt": "2026-01-01T00:00:00"
  }
}
```

##### Update Budget
```http
POST /update_budget
Content-Type: application/json

{
  "financialYear": "2026-2027",
  "schoolName": "Updated School Name",
  "totalGrant": 120000,
  "items": [...]
}
```

#### Credit Management

##### Get Credits
```http
GET /credits?financial_year=2026-2027
```

##### Add Credit
```http
POST /add_credit
Content-Type: application/json

{
  "date": "2026-01-15",
  "month": "January",
  "lineItems": [
    {
      "subItemDescription": "School Fees",
      "amount": 5000
    }
  ],
  "remarks": "Monthly school fees collection",
  "financialYear": "2026-2027"
}
```

##### Update Credit
```http
POST /update_credit/{index}
Content-Type: application/json

{
  "date": "2026-01-15",
  "month": "January",
  "lineItems": [...],
  "remarks": "Updated remarks",
  "financialYear": "2026-2027"
}
```

##### Delete Credit
```http
POST /delete_credit/{index}
Content-Type: application/x-www-form-urlencoded

financial_year=2026-2027
```

#### Debit Management

##### Get Debits
```http
GET /debits?financial_year=2026-2027
```

##### Add Debit
```http
POST /add_debit
Content-Type: application/json

{
  "date": "2026-01-15",
  "month": "January",
  "itemId": "pow1",
  "subItemDescription": "Exercise Books",
  "code": "TLM001",
  "description": "Purchase of exercise books",
  "amount": 2000,
  "supplierName": "Stationery Store",
  "position": "Bursar",
  "financialYear": "2026-2027"
}
```

##### Update Debit
```http
POST /update_debit/{index}
Content-Type: application/json

{
  "date": "2026-01-15",
  "month": "January",
  "itemId": "pow1",
  "subItemDescription": "Exercise Books",
  "code": "TLM001",
  "description": "Updated description",
  "amount": 2500,
  "supplierName": "Stationery Store",
  "position": "Bursar",
  "financialYear": "2026-2027"
}
```

##### Delete Debit
```http
POST /delete_debit/{index}
Content-Type: application/x-www-form-urlencoded

financial_year=2026-2027
```

#### Data Management

##### Clear All Registers
```http
POST /clear_registers
Content-Type: application/json

{
  "financialYear": "2026-2027"
}
```

**Response:**
```json
{
  "success": true,
  "message": "All registers cleared successfully"
}
```

### Data Storage

All data is stored in JSON files in the `data/` directory:

- `data/budgets.json` - Budget data
- `data/credits.json` - Credit entries
- `data/debits.json` - Debit entries

### Error Handling

All API endpoints return JSON responses with the following structure:

**Success Response:**
```json
{
  "success": true,
  "data": {...}
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Error message description"
}
```

### HTTP Status Codes

- `200` - Success
- `400` - Bad Request
- `404` - Not Found
- `500` - Internal Server Error

### Examples

#### JavaScript Example
```javascript
// Add a new credit
const creditData = {
  date: "2026-01-15",
  month: "January",
  lineItems: [
    { subItemDescription: "School Fees", amount: 5000 }
  ],
  remarks: "Monthly collection",
  financialYear: "2026-2027"
};

fetch('/add_credit', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(creditData)
})
.then(response => response.json())
.then(data => {
  if (data.success) {
    console.log('Credit added successfully');
  } else {
    console.error('Error:', data.error);
  }
});
```

#### Python Example
```python
import requests

# Add a new debit
debit_data = {
    "date": "2026-01-15",
    "month": "January",
    "itemId": "pow1",
    "subItemDescription": "Exercise Books",
    "code": "TLM001",
    "description": "Purchase of exercise books",
    "amount": 2000,
    "supplierName": "Stationery Store",
    "position": "Bursar",
    "financialYear": "2026-2027"
}

response = requests.post('http://localhost:5173/add_debit', json=debit_data)
result = response.json()

if result['success']:
    print("Debit added successfully")
else:
    print(f"Error: {result['error']}")
```
