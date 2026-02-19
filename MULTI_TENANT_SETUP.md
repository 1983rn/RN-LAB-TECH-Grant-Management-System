# Multi-Tenant Architecture Setup Guide

## Overview

The Grant Management System now supports multiple schools with complete data isolation. Each school operates as an independent tenant with their own data, while a developer can manage schools without accessing their financial records.

## Key Features

✅ **Complete Data Isolation**: Each school can only see their own data
✅ **Developer Dashboard**: Manage schools, subscriptions, and credentials
✅ **Subscription Management**: Track and control school access
✅ **Password Reset**: Generate one-time passwords for schools
✅ **Online Tracking**: Monitor which schools are currently active
✅ **Audit Logging**: All actions are logged with timestamps

## Installation & Migration

### Step 1: Install Dependencies

```bash
pip install flask flask-cors
```

### Step 2: Run Migration

This will convert your existing single-school data to multi-tenant format:

```bash
python migrate.py
```

The migration will:
- Create the multi-tenant database structure
- Migrate existing budget, credit, and debit data
- Create a default school account
- Create the developer account

### Step 3: Start the Application

```bash
python app.py
```

## Default Credentials

### Default School Account
- **Username**: `admin`
- **Password**: `admin123`
- **School**: NANJATI CDSS (or your existing school name)

### Developer Account
- **Username**: `juniornsambe@yahoo.com`
- **Password**: `blessings19831983/`
- **Access Method**: Type `devaccess` on the login screen

## User Roles

### School Administrator
- Access only their school's data
- Manage budget allocation
- Record credits and debits
- Generate reports
- Cannot see other schools' data

### Developer
- Add new schools
- Monitor school activity
- Manage subscriptions
- Lock/unlock schools
- Reset passwords
- Send messages to schools
- **CANNOT** access school financial data

## Developer Dashboard Features

### School Management
- **Add New School**: Create new school accounts with credentials
- **View All Schools**: See list of all registered schools
- **Lock/Unlock**: Control school access
- **Reset Password**: Generate OTP for schools

### Subscription Management
- **Track Status**: PAID, UNPAID, EXPIRED
- **Send Warnings**: Notify schools about expiring subscriptions
- **Auto-Lock**: Lock schools with expired subscriptions

### Monitoring
- **Online Tracking**: See which schools are currently logged in
- **Last Login**: Track school activity
- **Audit Logs**: View all system actions

## Security Features

### Data Isolation
- Every query filters by `school_id`
- Schools cannot access other schools' data
- Developer cannot access financial records

### Password Security
- Passwords are hashed using SHA-256
- One-time passwords expire after 24 hours
- Password reset requires OTP

### Audit Trail
- All actions are logged
- Includes timestamp, actor, and target
- IP addresses are recorded

## Database Schema

### Core Tables
- `schools`: School accounts and subscriptions
- `school_settings`: Settings per school per financial year
- `budget_items`: Budget allocations (multi-tenant)
- `credits`: Credit register (multi-tenant)
- `debits`: Debit register (multi-tenant)
- `document_sequences`: Document numbering per school
- `subscription_messages`: Messages to schools
- `school_sessions`: Online tracking
- `password_reset_tokens`: OTP management
- `audit_logs`: Action logging

### Indexes
- `school_id` indexed on all tenant tables
- `(school_id, financial_year)` composite indexes
- Unique constraints on document numbers per school

## API Endpoints

### Authentication
- `POST /login`: School and developer login
- `POST /logout`: Logout and end session

### Developer Only
- `GET /dev/dashboard`: Developer dashboard
- `POST /dev/add-school`: Add new school
- `POST /dev/reset-password/<id>`: Generate OTP
- `POST /dev/lock-school/<id>`: Lock school
- `POST /dev/unlock-school/<id>`: Unlock school
- `POST /dev/send-message/<id>`: Send message
- `POST /dev/send-expiry-warnings`: Bulk warnings

### School Only
- All existing endpoints (budget, credits, debits, etc.)
- Automatically filtered by logged-in school

## Adding a New School

1. Login as developer (type `devaccess` on login screen)
2. Click "Add New School"
3. Enter:
   - School Name
   - Username (unique)
   - Initial Password
   - Subscription End Date
4. School starts with empty data
5. Provide credentials to school administrator

## Password Reset Process

1. Developer generates OTP for school
2. OTP is displayed (valid for 24 hours)
3. School logs in with OTP
4. System forces password change
5. School sets new password

## Subscription Management

### Status Types
- **PAID**: Active subscription
- **UNPAID**: Not yet paid
- **EXPIRED**: Subscription ended
- **LIFETIME**: Never expires (developer only)

### Expiry Warnings
- Automatically send warnings 7 days before expiry
- Schools receive in-app messages
- Developer can manually send warnings

### Locking Schools
- Expired schools are automatically locked
- Locked schools cannot login
- Developer can manually lock/unlock

## Troubleshooting

### Migration Issues
If migration fails:
```bash
# Backup existing data
cp -r data data_backup

# Re-run migration
python migrate.py
```

### Login Issues
- Verify credentials are correct
- Check if school is locked
- Verify subscription status
- Check audit logs for details

### Data Not Showing
- Verify correct financial year is selected
- Check school_id in database
- Verify data was migrated correctly

## Best Practices

1. **Regular Backups**: Backup the database regularly
2. **Strong Passwords**: Use strong passwords for all accounts
3. **Monitor Activity**: Check audit logs regularly
4. **Update Subscriptions**: Keep subscriptions current
5. **Secure Developer Access**: Protect developer credentials

## Support

For technical support:
- **Developer**: RN-LAB-TECH-SOLUTIONS
- **Phone**: +265991332952
- **WhatsApp**: +265999630132
- **Email**: robertnsambe@gmail.com

## License

This system maintains the same license as the original application.
