# Grant Management System - Python Version

A comprehensive grant management system converted from React/TypeScript to Python Flask for managing school budgets, credits, and debits.

## Features

- **Dashboard**: Overview of budget, credits, and debits
- **Budget Management**: Initialize and manage budget allocations
- **Credit Register**: Track fund receipts and income
- **Debit Register**: Manage payments and expenses
- **Spending Tracking**: Visual reports and analytics
- **Data Management**: Clear and export functionality

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Access the application at `http://localhost:5176`

## File Structure

```
python-app/
├── app.py                 # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md             # This file
├── data/                # JSON data storage
│   ├── budgets.json      # Budget data
│   ├── credits.json      # Credit entries
│   └── debits.json      # Debit entries
├── templates/           # HTML templates
│   ├── base.html         # Base template
│   ├── index.html       # Dashboard
│   ├── budget.html      # Budget management
│   ├── credits.html     # Credit register
│   ├── debits.html      # Debit register
│   ├── tracking.html    # Spending tracking
│   └── initialize_budget.html # Budget initialization
├── static/              # Static files (CSS, JS, images)
└── docs/               # Documentation
```

## Usage

1. **Initialize Budget**: Start by setting up your budget allocation
2. **Add Credits**: Record fund receipts and income
3. **Add Debits**: Track payments and expenses
4. **Track Spending**: Monitor budget usage and remaining funds
5. **Manage Data**: Clear registers or export data as needed

## Data Storage

The application uses JSON files for data storage:
- All data is stored in the `data/` directory
- Automatic backup and recovery
- Easy data export and import

## Development

The application runs in development mode with:
- Auto-reload on code changes
- Debug mode enabled
- Detailed error logging

## Original React Version

This is a Python conversion of the original React/TypeScript application. The original React code is preserved in the parent directory for reference.

## License

This project maintains the same license as the original React application.
