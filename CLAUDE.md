# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **fictional financial data simulation project** that generates realistic-looking PDF financial documents for demonstration, testing, and educational purposes. All data is entirely fictional.

### Fictional Characters
- **Bob Doe** (47): Security Guard at Acme Technology Corp, $95k/year
- **Jane Doe** (45): Elementary School Teacher at Metro Nashville Public Schools, $65k/year
- **Location**: Nashville, TN
- **Household Income**: $160,000 combined annual

### What This Project Generates

1. **Checking Account Statements** (12 monthly PDFs for 2024)
   - Bi-monthly paychecks from both employers
   - Mortgage, vehicle loans, insurance, utilities
   - Groceries, gas, dining, shopping transactions
   - Transfer to savings account
   - Jane's gambling expenses (DraftKings)

2. **Savings Account Statements** (12 monthly PDFs for 2024)
   - High-yield savings at 4.25% APY
   - Monthly $500 transfers from checking
   - Interest accrual tracking
   - Occasional withdrawals for larger expenses

3. **Retirement Account Statements** (2 annual PDFs for 2024)
   - Bob's Fidelity 401(k): $142,500 → $169,162
   - Jane's TIAA 403(b): $98,750 → $116,447
   - Quarterly breakdowns and investment allocations

4. **Tax Return (Form 1040)** (1 annual PDF for 2023)
   - Married Filing Jointly tax return
   - Combined W-2 income from both employers
   - Standard deduction and tax calculations
   - Federal withholding and refund/payment details

5. **Utility Bills** (48 PDFs for 2024 - 4 types × 12 months)
   - Electric bills (Nashville Electric Service) - $140-$210/month variable
   - Gas bills (Piedmont Natural Gas) - $45-$85/month variable
   - Water bills (Metro Water Services) - ~$65/month with sewer charges
   - Internet bills (Comcast Xfinity) - $75/month fixed

## Project Structure

```
bobandjanedoe/
├── generate_statements.py              # Checking account generator
├── generate_savings_statements.py      # Savings account generator
├── generate_retirement_statements.py   # Retirement account generator
├── generate_tax_return.py              # Form 1040 tax return generator
├── generate_utility_bills.py           # Utility bills generator (electric, gas, water, internet)
├── requirements.txt                    # Python dependencies (fpdf2)
├── README.md                          # Comprehensive documentation
└── bank_statements/                   # Output directory for all PDFs
```

## Technology Stack

- **Python 3.8+**: Core language
- **fpdf2**: PDF generation library
- **Standard libraries**: datetime, calendar, random, os

## Key Implementation Details

### generate_statements.py
- Generates checking account statements with realistic transaction patterns
- Bi-monthly paycheck deposits on the 15th and last day of month
- Fixed monthly expenses (mortgage, insurance, subscriptions)
- Variable expenses with randomization (utilities, groceries, gas, dining)
- Running balance calculations throughout the month
- Professional PDF layout with header, footer, account summary

### generate_savings_statements.py
- High-yield savings account with 4.25% APY
- Monthly interest calculations using APY/12
- Consistent $500 monthly transfers from checking
- 30% probability of withdrawal each month for larger expenses
- Year-to-date interest tracking
- Green-themed PDF design to differentiate from checking

### generate_retirement_statements.py
- Separate 401(k) and 403(b) statement generation
- Contribution calculations based on salary percentages
- Investment gain modeling (~10-12% annual returns)
- Quarterly activity breakdowns
- Investment fund allocation tables
- Administrator-specific branding (Fidelity green vs TIAA blue)

### generate_tax_return.py
- Generates Form 1040 (U.S. Individual Income Tax Return)
- Married Filing Jointly filing status for 2023 tax year
- Calculates total income from W-2 wages ($95k + $65k = $160k)
- Includes interest income from savings account
- Applies 2023 standard deduction ($27,700)
- Calculates federal tax using 2023 MFJ tax brackets
- Shows federal withholding and refund/payment calculation
- Professional IRS form layout with disclaimer

### generate_utility_bills.py
- Generates monthly bills for 4 utility types (48 bills total)
- **Electric** (Nashville Electric Service): Variable bills $140-$210 with seasonal usage patterns (higher in summer/winter)
- **Gas** (Piedmont Natural Gas): Variable bills $45-$85 with winter heating usage
- **Water** (Metro Water Services): Bills ~$65 including water usage and sewer charges
- **Internet** (Comcast Xfinity): Fixed $75/month bills for 200 Mbps service
- Bill amounts align with charges in checking account statements
- Each bill includes usage details, billing period, due date, and charges breakdown
- Color-coded company branding (blue for electric, orange for gas, green for water, black for internet)

## Usage Instructions

Run each script independently to generate the respective PDFs:

```bash
# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows

# Generate checking statements
python generate_statements.py

# Generate savings statements
python generate_savings_statements.py

# Generate retirement statements
python generate_retirement_statements.py

# Generate tax return
python generate_tax_return.py

# Generate utility bills
python generate_utility_bills.py
```

All PDFs are output to the `bank_statements/` directory.

## Development Guidelines

### If Modifying Financial Parameters

1. **Checking Account**: Edit `MONTHLY_EXPENSES` dict and income variables in `generate_statements.py`
2. **Savings Account**: Modify `ACCOUNT_INFO["apy"]` and `MONTHLY_TRANSFER` in `generate_savings_statements.py`
3. **Retirement**: Update `BOB_401K` and `JANE_403B` dictionaries in `generate_retirement_statements.py`
4. **Tax Return**: Modify `INCOME` dict and `TAX_CONSTANTS_2023` in `generate_tax_return.py`
5. **Utility Bills**: Update `UTILITIES` dict in `generate_utility_bills.py` to change bill amounts, billing dates, or company information

### If Adding New Features

- Follow the existing PDF class structure (inheriting from FPDF)
- Maintain the realistic disclaimer footers
- Use consistent date formatting and transaction patterns
- Ensure running balance calculations are accurate

### If Updating for a Different Year

- Change the `year = 2024` variable in each main() function
- Update retirement account beginning balances accordingly
- Consider adjusting investment return rates for the target year

## Important Reminders

- All data is **fictional** - SSNs, account numbers, names, addresses are made up
- This is for **demonstration/testing/educational purposes only**
- PDFs include disclaimer footers indicating they are simulated
- Do not use this project for illegal activities

## Testing

To verify the generators work correctly:

1. Ensure virtual environment is activated
2. Run each generator script
3. Check that PDFs are created in `bank_statements/` directory
4. Open a few PDFs to verify formatting and data accuracy
5. Verify balance calculations make sense month-over-month

## Dependencies

- **fpdf2** (v2.8.5): Primary dependency for PDF generation
- No external API calls or network dependencies
- Runs entirely locally

## Important Notes on Utility Bills & Bank Statements

The utility bill charges are designed to match the ranges in the checking account statements:
- **Electric**: Generated with variable amounts ($140-$210) that align with `Nashville Electric Service` charges in bank statements
- **Gas**: Generated with variable amounts ($45-$85) that align with `Piedmont Natural Gas` charges in bank statements
- **Water**: Generated at ~$65 that aligns with `Metro Water Services` charges in bank statements
- **Internet**: Generated at fixed $75 that aligns with `Internet - Comcast` charges in bank statements

Note: Due to randomization, the exact amounts may differ slightly between the utility bills and bank statement transactions. For perfectly matching amounts, you would need to generate bank statements and utility bills with the same random seed or modify the generators to share transaction data.

## Potential Enhancements

If extending this project, consider:
- Adding W-2 form generator (individual wage statements from employers)
- Creating 1099-INT forms for savings interest
- Generating credit card statements
- Creating paycheck stub PDFs
- Adding state tax return (Tennessee has no state income tax)
- Implementing a configuration file for easy parameter changes
- Adding command-line arguments for year/month selection
- Creating a web interface for on-demand generation
- Synchronizing utility bill amounts with exact bank statement transactions

## Repository Information

- **GitHub**: https://github.com/jamiechurch/bobandjanedoe
- **Primary Language**: Python
- **License**: Demonstration project, use responsibly
