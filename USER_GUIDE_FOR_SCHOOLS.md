# GRANT MANAGEMENT SYSTEM - USER GUIDE FOR SCHOOLS

## Table of Contents
1. [Getting Started](#getting-started)
2. [System Settings](#system-settings)
3. [Budget Allocation](#budget-allocation)
4. [Credit Register](#credit-register)
5. [Debit Register](#debit-register)
6. [Spending Tracking](#spending-tracking)
7. [Generating Documents](#generating-documents)
8. [Exporting Data](#exporting-data)

---

## 1. GETTING STARTED

### First Time Login
1. Open your web browser (Chrome, Firefox, or Edge)
2. Go to: `http://localhost:5176`
3. Enter your school credentials:
   - **Username**: Provided by administrator
   - **Password**: Provided by administrator
4. Click **Login**

### Understanding the Dashboard
After login, you'll see:
- **Total Grant**: Your school's total budget allocation
- **Total Budgeted**: Amount allocated across all POWs
- **Total Credited**: Funds received
- **Total Spent**: Payments made
- **Balance**: Remaining funds

---

## 2. SYSTEM SETTINGS

### Step 1: Configure School Details
1. Click **Settings** in the navigation menu
2. Fill in **School Details**:
   - School Name (auto-filled)
   - School Address
   - Total Grant Amount (IMPORTANT: Enter your total budget here)

### Step 2: Set Financial Year
1. In Settings, select your **Financial Year** (e.g., 2026-2027)
2. Click **Update Financial Year**
3. This determines which data you're working with

### Step 3: Configure Signatories
Fill in the following fields:
- **Compiled By**: Name of person preparing the budget
- **Entered By**: Name of data entry person
- **Authorizing Officer**: Name and title
- **Counter Sign**: Name and title

4. Click **Save Settings**

---

## 3. BUDGET ALLOCATION

### Understanding POWs (Program of Works)
Your budget has **16 POWs** with **42 line items** total:
- POW 1: Facilitating office operations (14 items)
- POW 2: Management of examinations (1 item)
- POW 3: Budget meetings (2 items)
- POW 4: SMASSE (2 items)
- POW 5: Sporting activities (3 items)
- POW 6: Special needs education (1 item)
- POW 7: Teaching materials (3 items)
- POW 8: HIV/AIDS & first aid (2 items)
- POW 9: Infrastructure maintenance (2 items)
- POW 10: Subscriptions (2 items)
- POW 11: Teacher training (3 items)
- POW 12: Payment vouchers (2 items)
- POW 13: Sanitary pads (1 item)
- POW 14: PPEs (1 item)
- POW 15: Boarding expenses (1 item)
- POW 16: Education visits (2 items)

### Step 1: Access Budget Allocation
1. Click **Budget Allocation** in the menu
2. You'll see all 42 budget line items

### Step 2: Allocate Annual Budget
For each line item:
1. Enter amount in **Annual Allocation** column
2. The system calculates remaining balance automatically

### Step 3: Allocate Monthly Budget
For each line item:
1. Enter amounts for each month (April to March)
2. System shows:
   - **Total Budgeted**: Sum of monthly allocations
   - **Balance**: Annual allocation minus monthly total

### Step 4: Save Your Budget
1. Click **Save All Changes** button
2. Wait for confirmation message
3. System validates that monthly totals don't exceed annual allocation

### Tips:
- ✅ Annual allocation should match your total grant
- ✅ Monthly allocations should not exceed annual allocation
- ✅ Distribute funds based on when you expect to spend
- ✅ Save frequently to avoid losing work

---

## 4. CREDIT REGISTER

### What is Credit Register?
Records all funds received by your school (income/receipts)

### Step 1: Add a Credit Entry
1. Click **Credit Register** in the menu
2. Click **Add Credit** button
3. Fill in the form:
   - **Date**: When funds were received
   - **Month**: Select the month
   - **Remarks**: Description (e.g., "First Quarter Grant")

### Step 2: Allocate Credit to POWs
For each POW that received funds:
1. Select the **POW Item** from dropdown
2. Enter the **Amount** received
3. Click **Add Line Item** to add more POWs
4. Click **Save Credit**

### Example:
```
Date: 15/04/2026
Month: April
Remarks: First Quarter Grant Release

Line Items:
- POW 1 (Wages): MWK 500,000
- POW 7 (Textbooks): MWK 300,000
- POW 9 (Maintenance): MWK 200,000
Total: MWK 1,000,000
```

### Step 3: View Credit History
- All credits appear in the table below
- Shows: Date, Month, Amount, Remarks
- Click **Delete** to remove incorrect entries

---

## 5. DEBIT REGISTER

### What is Debit Register?
Records all payments made by your school (expenses)

### Step 1: Add a Debit Entry
1. Click **Debit Register** in the menu
2. Click **Add Debit** button
3. Fill in the form:
   - **Date**: Payment date
   - **Month**: Select month
   - **POW Item**: Select what you're paying for
   - **Description**: What was purchased
   - **Amount**: Payment amount
   - **Supplier Name**: Who received payment
   - **Position**: Supplier's role (if applicable)

### Step 2: Save the Debit
1. Review all information
2. Click **Save Debit**
3. System automatically generates:
   - **GP10 Number**: Sequential voucher number
   - **Loose Minute Number**: Generated when viewing document
   - **Receipt Number**: Generated when viewing receipt

### Step 3: View Available Funds
The system shows for each POW:
- **Budgeted**: Amount allocated
- **Credited**: Funds received
- **Spent**: Payments made
- **Balance**: Available funds (Credited - Spent)

### Important Rules:
- ⚠️ You can only spend from POWs that have received credits
- ⚠️ Cannot spend more than available balance
- ⚠️ Each payment must be linked to a specific POW

---

## 6. SPENDING TRACKING

### View Spending Reports
1. Click **Spending Tracking** in the menu
2. See comprehensive reports:
   - Spending by POW
   - Monthly spending trends
   - Budget vs Actual comparison

### Understanding the Reports

#### POW Spending Table
Shows for each POW:
- **Budgeted**: Annual allocation
- **Spent**: Total payments
- **Balance**: Remaining budget
- **% Used**: Spending percentage

#### Monthly Spending Chart
- Visual graph of spending per month
- Helps identify spending patterns
- Compare against budget

#### Budget Utilization
- Overall spending percentage
- Alerts if overspending
- Shows remaining funds

---

## 7. GENERATING DOCUMENTS

### GP10 Payment Voucher
1. Go to **Debit Register**
2. Find the payment entry
3. Click **GP10** button
4. Document shows:
   - GP10 number
   - Payment details
   - Supplier information
   - Signature lines
5. Click **Print** to print the voucher

### Loose Minute
1. Go to **Debit Register**
2. Click **Loose Minute** button
3. Document shows:
   - Loose Minute number
   - Payment justification
   - Authorization details
4. Click **Print**

### Payment Receipt
1. Go to **Debit Register**
2. Click **Receipt** button
3. Document shows:
   - Receipt number
   - Amount received
   - Supplier acknowledgment
4. Click **Print**

### Document Numbering
- **GP10**: Sequential per financial year (GP10-001, GP10-002...)
- **Loose Minute**: Sequential per financial year (LM-001, LM-002...)
- **Receipt**: Sequential per financial year (RCP-001, RCP-002...)

---

## 8. EXPORTING DATA

### Export Budget to Excel
1. Go to **Budget Allocation**
2. Click **Export to Excel** button
3. Excel file downloads with:
   - Malawi Government logo
   - All 42 budget line items
   - Monthly allocations
   - Totals and balances
4. Use for reporting and printing

### Export Options (Future)
- Credit Register export
- Debit Register export
- Spending reports export

---

## COMMON WORKFLOWS

### Workflow 1: Start of Financial Year
1. Go to **Settings** → Set Financial Year
2. Enter **Total Grant** amount
3. Go to **Budget Allocation** → Allocate funds to POWs
4. Save budget

### Workflow 2: Receiving Funds
1. Go to **Credit Register**
2. Add credit entry with date and amount
3. Allocate to specific POWs
4. Save credit

### Workflow 3: Making a Payment
1. Check **Debit Register** → Available Funds
2. Ensure POW has sufficient balance
3. Click **Add Debit**
4. Fill in payment details
5. Save debit
6. Generate GP10, Loose Minute, and Receipt

### Workflow 4: Monthly Reporting
1. Go to **Spending Tracking**
2. Review spending by POW
3. Export budget to Excel
4. Print reports for submission

---

## TROUBLESHOOTING

### Cannot Save Budget
- ✅ Check that monthly totals don't exceed annual allocation
- ✅ Ensure all required fields are filled
- ✅ Try refreshing the page and logging in again

### Cannot Add Debit
- ✅ Ensure POW has received credits first
- ✅ Check available balance is sufficient
- ✅ Verify all required fields are filled

### Missing Data
- ✅ Check you're in the correct Financial Year
- ✅ Go to Settings and verify Financial Year selection

### Subscription Expired
- ✅ Contact system administrator
- ✅ Payment required to renew subscription

---

## BEST PRACTICES

### Daily Tasks
- ✅ Record all receipts immediately in Credit Register
- ✅ Record all payments immediately in Debit Register
- ✅ Generate documents (GP10, Loose Minute, Receipt) for each payment

### Weekly Tasks
- ✅ Review spending tracking reports
- ✅ Check available balances before making payments
- ✅ Verify all entries are correct

### Monthly Tasks
- ✅ Export budget to Excel for records
- ✅ Review monthly spending vs budget
- ✅ Prepare reports for submission

### End of Quarter
- ✅ Generate comprehensive spending reports
- ✅ Review budget utilization
- ✅ Plan for next quarter spending

---

## SUPPORT

### Need Help?
- **Technical Issues**: Contact system administrator
- **Training**: Request additional training session
- **Password Reset**: Contact administrator for OTP

### System Requirements
- **Browser**: Chrome, Firefox, or Edge (latest version)
- **Internet**: Not required (runs locally)
- **Screen**: Minimum 1024x768 resolution

---

## APPENDIX: POW CODES REFERENCE

### POW 1 - Facilitating Office Operations
- 2211012204: Wages for support staff
- 2211011203: Public transport
- 2211011401: Heating and lighting
- 2211011402: Telephone charges
- 2211011405: Water and sanitation
- 2211011502: Consumable stores
- 2211011504: Postage
- 2211011505: Printing cost
- 2211011406: Publication and advertisement
- 2211011506: Stationery
- 2211011507: Uniform and protective wear
- 2211012401: Fuel and Lubricants
- 2211012321: Subscriptions
- 2211010251: Purchase of plant and office equipment

### POW 2 - Management of Examinations
- 2211011803: Examinations

### POW 3 - Budget Meetings
- 2211012401: Fuel or public transport
- 2211011204: Subsistence allowance

### POW 4 - SMASSE
- 2211012401: Fuel or public transport
- 2211011204: Subsistence allowance

### POW 5 - Sporting Activities
- 2211011805: Sporting equipment
- 2211012401: Fuel or public transport
- 2211011204: Subsistence allowance

### POW 6 - Special Needs Education
- 2211011806: Purchase of special needs materials

### POW 7 - Teaching Materials
- 2211011807: Science consumables
- 2211011804: Text books
- 2211011808: Purchase of school supplies

### POW 8 - HIV/AIDS & First Aid
- 2211011614: HIV/AIDS services
- 2211011601: Drugs

### POW 9 - Infrastructure Maintenance
- 2211012501: Maintenance of buildings
- 2211012504: Maintenance of water supplies

### POW 10 - Subscriptions
- 2211012321: COSOMA Subscription
- 2211012321: Computer Service Subscription

### POW 11 - Teacher Training
- 2211011502: Consumables
- 2211011204: Subsistence Allowances
- 2211011203: Public transport or fuel

### POW 12 - Payment Vouchers
- 2211011204: Subsistence Allowances
- 2211011203: Public transport or fuel

### POW 13 - Sanitary Pads
- 2211011502: Consumables

### POW 14 - PPEs
- 2211011502: Consumables

### POW 15 - Boarding Expenses
- 2211011801: Boarding expenses

### POW 16 - Education Visits
- 2211011204: Subsistence Allowances
- 2211011203: Public transport or fuel

---

**Version**: 1.0  
**Last Updated**: January 2025  
**System**: Grant Management System - Multi-Tenant Edition
