# FIRST TIME USER GUIDE
## Complete Setup: Login to Grant Summary

---

## 🎯 OVERVIEW
This guide takes you through the complete setup process for first-time users, from login to viewing your Grant Summary dashboard.

**Time Required**: 15-20 minutes  
**What You'll Accomplish**: Full system setup and first grant summary report

---

## STEP 1: LOGIN (2 minutes)

### What You Need
- Username (provided by administrator)
- Password (provided by administrator)
- Web browser (Chrome, Firefox, or Edge)

### How to Login
1. Open your web browser
2. Type in address bar: `http://localhost:5176`
3. Press Enter
4. You'll see the login page

### Enter Your Credentials
```
Username: [Your school username]
Password: [Your password]
```

5. Click the **Login** button

### What Happens Next
- System validates your credentials
- You're redirected to the Home/Welcome page
- You'll see your school name at the top

✅ **You're now logged in!**

---

## STEP 2: CONFIGURE SETTINGS (5 minutes)

### Why This is Important
Settings contain your school's basic information and total grant amount. This MUST be done first before anything else.

### Navigate to Settings
1. Look at the top navigation menu
2. Click on **Settings**

### Fill in School Details

#### Section A: School Information
```
School Name: [Auto-filled with your school name]
School Address: [Enter your complete school address]
Example: P.O. Box 123, Lilongwe, Malawi
```

#### Section B: Financial Year
```
Financial Year: Select from dropdown
Example: 2026-2027
```
- This determines which budget period you're working with
- Click **Update Financial Year** button

#### Section C: Total Grant Amount ⚠️ CRITICAL
```
Total Grant: [Enter your total budget allocation]
Example: 5000000 (for MWK 5,000,000)
```
**IMPORTANT**: This is the MOST important field. Enter the total amount of grant your school received from the government.

#### Section D: Signatories (Optional but Recommended)
```
Compiled By: [Name of person preparing budget]
Entered By: [Name of data entry person]
Authorizing Officer: [Name and title]
Authorizing Appointment: [Position/Title]
Counter Sign: [Name]
Counter Appointment: [Position/Title]
Ministry/Department: Education (default)
```

### Save Your Settings
1. Scroll to bottom of page
2. Click **Save Settings** button
3. Wait for confirmation message: "Settings saved successfully"

✅ **Settings configured!**

---

## STEP 3: ALLOCATE BUDGET (8 minutes)

### Navigate to Budget Allocation
1. Click **Budget Allocation** in the top menu
2. You'll see a table with 42 rows (all your budget line items)

### Understanding the Budget Table

#### Columns Explained
- **POW No**: Program of Work number (1-16)
- **POW Name**: Description of the program
- **Sub Activity**: Specific activity under the POW
- **Sub Item Description**: Detailed description
- **Code**: Government accounting code
- **Annual Allocation**: Total amount for the year
- **Monthly Columns**: April to March allocations
- **Total Budgeted**: Sum of monthly allocations
- **Balance**: Annual minus monthly total

### How to Allocate Budget

#### Method 1: Annual Allocation Only (Quick Method)
1. For each row, enter amount in **Annual Allocation** column
2. Leave monthly columns at zero for now
3. Example:
   ```
   POW 1 - Wages: 500,000
   POW 1 - Transport: 200,000
   POW 2 - Examinations: 300,000
   ```

#### Method 2: Monthly Allocation (Detailed Method)
1. Enter amount in **Annual Allocation** column
2. Distribute across months (April to March)
3. Example:
   ```
   POW 1 - Wages: Annual = 600,000
   - April: 50,000
   - May: 50,000
   - June: 50,000
   ... (continue for all months)
   Total Budgeted: 600,000
   Balance: 0
   ```

### Budget Allocation Tips
✅ **Total of all Annual Allocations should equal your Total Grant**
✅ **Monthly allocations should not exceed Annual Allocation**
✅ **Distribute based on when you expect to spend**
✅ **Focus on high-priority POWs first**

### Common POWs to Allocate
```
POW 1: Office Operations (Wages, Transport, Utilities)
POW 2: Examinations
POW 7: Teaching Materials (Textbooks, Science supplies)
POW 9: Infrastructure Maintenance
POW 15: Boarding Expenses (if applicable)
```

### Save Your Budget
1. Scroll to bottom of page
2. Click **Save All Changes** button
3. Wait for confirmation: "Budget saved successfully"

✅ **Budget allocated!**

---

## STEP 4: RECORD FIRST CREDIT (3 minutes)

### What is a Credit?
A credit is money received by your school (income/receipt). You must record credits before you can make payments.

### Navigate to Credit Register
1. Click **Credit Register** in the menu
2. Click **Add Credit** button

### Fill in Credit Details
```
Date: [Date funds were received]
Example: 15/04/2026

Month: [Select from dropdown]
Example: April

Remarks: [Description of the funds]
Example: "First Quarter Grant Release"
```

### Allocate Credit to POWs
1. Click **Add Line Item** button
2. For each POW that received funds:
   ```
   POW Item: [Select from dropdown]
   Example: POW 1 - Wages for support staff
   
   Amount: [Enter amount]
   Example: 500000
   ```
3. Click **Add Line Item** again to add more POWs
4. Repeat until all funds are allocated

### Example Credit Entry
```
Date: 15/04/2026
Month: April
Remarks: First Quarter Grant Release

Line Items:
- POW 1 (Wages): 500,000
- POW 1 (Transport): 200,000
- POW 7 (Textbooks): 300,000
- POW 9 (Maintenance): 200,000

Total Credit: 1,200,000
```

### Save the Credit
1. Review all information
2. Click **Save Credit** button
3. Wait for confirmation

✅ **First credit recorded!**

---

## STEP 5: RECORD FIRST DEBIT (3 minutes)

### What is a Debit?
A debit is a payment made by your school (expense). You can only pay from POWs that have received credits.

### Navigate to Debit Register
1. Click **Debit Register** in the menu
2. Review **Available Funds** section to see balances
3. Click **Add Debit** button

### Fill in Payment Details
```
Date: [Payment date]
Example: 20/04/2026

Month: [Select from dropdown]
Example: April

POW Item: [Select what you're paying for]
Example: POW 1 - Wages for support staff

Description: [What was purchased/paid]
Example: "Monthly wages for support staff - April 2026"

Amount: [Payment amount]
Example: 150000

Supplier Name: [Who received payment]
Example: "John Banda"

Position: [Supplier's role]
Example: "Support Staff"
```

### Save the Debit
1. Review all information
2. Click **Save Debit** button
3. System automatically generates:
   - GP10 Number (e.g., GP10-001)
   - Document numbers for printing

✅ **First payment recorded!**

---

## STEP 6: VIEW GRANT SUMMARY (2 minutes)

### Navigate to Grant Summary
1. Click **Grant Summary** or **Dashboard** in the menu
2. You'll see your complete financial overview

### Understanding Grant Summary

#### Top Summary Cards
```
┌─────────────────────────────────────────────┐
│ Total Grant: MWK 5,000,000                  │
│ (From Settings)                             │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ Total Budgeted: MWK 5,000,000               │
│ (Sum of all POW allocations)                │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ Total Credited: MWK 1,200,000               │
│ (Funds received)                            │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ Total Spent: MWK 150,000                    │
│ (Payments made)                             │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ Balance: MWK 1,050,000                      │
│ (Credited - Spent)                          │
└─────────────────────────────────────────────┘
```

#### Spending by POW Table
Shows for each POW:
- Budgeted amount
- Amount spent
- Remaining balance
- Percentage used

#### Monthly Spending Chart
- Visual graph showing spending trends
- Compare across months
- Identify spending patterns

#### Recent Transactions
- Latest credits received
- Latest payments made
- Quick overview of activity

✅ **Grant Summary complete!**

---

## STEP 7: GENERATE DOCUMENTS (Optional - 2 minutes)

### Print Payment Documents
1. Go back to **Debit Register**
2. Find your payment entry
3. Click buttons to generate:

#### GP10 Payment Voucher
- Click **GP10** button
- Review document
- Click **Print** to print

#### Loose Minute
- Click **Loose Minute** button
- Review justification
- Click **Print** to print

#### Payment Receipt
- Click **Receipt** button
- Review receipt
- Click **Print** to print

✅ **Documents generated!**

---

## 🎉 CONGRATULATIONS!

You have successfully:
✅ Logged into the system
✅ Configured school settings
✅ Allocated your budget
✅ Recorded your first credit
✅ Recorded your first payment
✅ Viewed your grant summary
✅ Generated payment documents

---

## 📊 YOUR SYSTEM IS NOW READY FOR DAILY USE

### Daily Operations Going Forward

#### When You Receive Funds
1. Go to **Credit Register**
2. Add credit entry
3. Allocate to POWs

#### When You Make Payments
1. Check **Available Funds** in Debit Register
2. Add debit entry
3. Generate documents (GP10, Loose Minute, Receipt)

#### Weekly Review
1. Check **Grant Summary**
2. Review spending by POW
3. Monitor balances

#### Monthly Tasks
1. Export budget to Excel
2. Generate reports
3. Plan next month's spending

---

## ⚠️ IMPORTANT REMINDERS

### Critical Rules
1. **Always enter Total Grant in Settings first**
2. **Record credits before making payments**
3. **Cannot spend more than available balance**
4. **Save your work frequently**
5. **Generate documents for every payment**

### Data Flow
```
Settings (Total Grant)
    ↓
Budget Allocation (Plan spending)
    ↓
Credit Register (Record funds received)
    ↓
Debit Register (Record payments)
    ↓
Grant Summary (View reports)
```

---

## 🆘 TROUBLESHOOTING

### Cannot Save Budget
**Problem**: Error when clicking "Save All Changes"
**Solution**: 
- Check monthly totals don't exceed annual allocation
- Ensure all required fields are filled
- Refresh page and try again

### Cannot Add Payment
**Problem**: Error when adding debit
**Solution**:
- Ensure POW has received credits first
- Check available balance is sufficient
- Verify all required fields are filled

### Numbers Don't Match
**Problem**: Grant Summary shows wrong totals
**Solution**:
- Verify Total Grant in Settings is correct
- Check all budget allocations are saved
- Ensure you're in correct Financial Year

### Missing Data
**Problem**: Cannot see budget or transactions
**Solution**:
- Go to Settings
- Verify Financial Year is correct
- Change if needed and check again

---

## 📞 NEED HELP?

### Contact Support
- **Technical Issues**: Contact system administrator
- **Training**: Request additional training session
- **Password Reset**: Contact administrator for OTP
- **Questions**: Refer to USER_GUIDE_FOR_SCHOOLS.md

### System Access
- **URL**: http://localhost:5176
- **Browser**: Chrome, Firefox, or Edge (latest version)
- **Support Hours**: [Contact administrator]

---

## 📚 NEXT STEPS

### Learn More
1. Read **USER_GUIDE_FOR_SCHOOLS.md** for detailed information
2. Review **QUICK_START_GUIDE.md** for daily operations
3. Practice adding more credits and debits
4. Explore Spending Tracking reports

### Best Practices
1. Record transactions daily
2. Review reports weekly
3. Export data monthly
4. Keep documents organized

---

**Version**: 1.0  
**Last Updated**: January 2025  
**System**: Grant Management System - Multi-Tenant Edition

---

## ✅ CHECKLIST FOR FIRST-TIME SETUP

Print this checklist and tick off as you complete each step:

- [ ] Step 1: Logged in successfully
- [ ] Step 2: Configured Settings (School details, Financial Year, Total Grant)
- [ ] Step 3: Allocated Budget to all POWs
- [ ] Step 4: Recorded first Credit entry
- [ ] Step 5: Recorded first Debit entry
- [ ] Step 6: Viewed Grant Summary dashboard
- [ ] Step 7: Generated payment documents (GP10, Loose Minute, Receipt)
- [ ] Verified all numbers match in Grant Summary
- [ ] Bookmarked system URL for easy access
- [ ] Saved administrator contact information

**Setup Complete!** 🎉
