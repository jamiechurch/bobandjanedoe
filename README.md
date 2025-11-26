# Bob and Jane Doe - Fictional Financial Simulation

A comprehensive fictional financial data simulation for a married couple in Nashville, TN. This project generates realistic-looking PDF financial documents including bank statements, savings account statements, retirement account statements, and W2 tax forms.

## Overview

This project creates a complete financial paper trail for fictional characters "Bob and Jane Doe" for the year 2024. All data is entirely fictional and generated for demonstration, testing, or educational purposes.

## Fictional Characters

### Bob Doe
- Age: 47 years old (DOB: March 15, 1977)
- Occupation: Security Guard at Acme Technology Corp
- Annual Salary: $95,000
- Retirement: Fidelity 401(k) with $169,162 ending balance
- SSN: 000-00-0000 (fictional)

### Jane Doe
- Age: 45 years old (DOB: August 22, 1979)
- Occupation: Elementary School Teacher at Metro Nashville Public Schools
- Annual Salary: $65,000
- Retirement: TIAA 403(b) with $116,447 ending balance
- SSN: 000-00-0001 (fictional)

### Household Details
- Address: 456 Maple Street, Nashville, TN 37215
- Combined Annual Income: $160,000
- Joint checking and savings accounts at First National Bank of Nashville

## Financial Profile Summary

### Assets & Accounts

**Checking Account** (Account #****4827)
- Starting Balance: $3,500.00
- Monthly Income: ~$9,671.64 (bi-monthly direct deposits)
- Major expenses include mortgage, vehicle loans, insurance, utilities

**Savings Account** (Account #****9821)
- High-Yield Savings at 4.25% APY
- Starting Balance: $8,500.00
- Monthly contribution: $500.00 transfer from checking
- Occasional withdrawals for larger expenses

**Retirement Accounts**
- Bob's 401(k): $142,500 → $169,162 (18.7% growth)
- Jane's 403(b): $98,750 → $116,447 (17.9% growth)

### Major Expenses

**Housing**
- Mortgage: $2,215.27/month (30-year loan on $375k @ 4% including escrow)

**Vehicles**
- Ford F-150 Truck: $504/month
- Harley Davidson Motorcycle: $385/month
- Auto Insurance: $233/month
- Motorcycle Insurance: $75/month

**Other Regular Expenses**
- Health Insurance: $350/month
- Life Insurance: $85/month
- Utilities: ~$250-350/month
- Cell Phone: $140/month
- Internet: $75/month
- Streaming Services: ~$48/month
- Gym Membership: $50/month
- Groceries: ~$600-800/month
- Gas: ~$300-400/month
- Dining Out: ~$250-400/month
- Jane's DraftKings: $700/month (gambling limit)

## Generated Documents

The project generates the following PDF documents in the `bank_statements/` directory:

### Checking Account Statements (12 files)
- `DoE_Statement_2024_01_January.pdf` through `DoE_Statement_2024_12_December.pdf`
- Shows bi-monthly paychecks, all expenses, transfers to savings
- Realistic transaction patterns including groceries, gas, dining, shopping

### Savings Account Statements (12 files)
- `DoE_Savings_2024_01_January.pdf` through `DoE_Savings_2024_12_December.pdf`
- Shows monthly $500 transfers from checking
- Interest accrual at 4.25% APY
- Occasional withdrawals for larger expenses

### Retirement Account Statements (2 files)
- `Bob_Doe_401k_2024_Annual_Statement.pdf`
  - Comprehensive annual statement with quarterly breakdowns
  - Investment holdings in Fidelity funds
  - Contribution details and beneficiary information

- `Jane_Doe_403b_2024_Annual_Statement.pdf`
  - Comprehensive annual statement with quarterly breakdowns
  - Investment holdings in TIAA funds
  - Contribution details and beneficiary information

### W2 Tax Forms (mentioned but not present)
- W2s for both Bob and Jane would be in this collection

## Project Structure

```
bobandjanedoe/
├── README.md                              # This file
├── CLAUDE.md                              # Claude Code guidance file
├── generate_statements.py                 # Checking account statement generator
├── generate_savings_statements.py         # Savings account statement generator
├── generate_retirement_statements.py      # Retirement account statement generator
├── requirements.txt                       # Python dependencies
├── venv/                                  # Python virtual environment
└── bank_statements/                       # Output directory for all PDFs
    ├── DoE_Statement_2024_01_January.pdf
    ├── DoE_Statement_2024_02_February.pdf
    ├── ... (10 more monthly statements)
    ├── DoE_Savings_2024_01_January.pdf
    ├── DoE_Savings_2024_02_February.pdf
    ├── ... (10 more monthly statements)
    ├── Bob_Doe_401k_2024_Annual_Statement.pdf
    └── Jane_Doe_403b_2024_Annual_Statement.pdf
```

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone this repository:
```bash
git clone https://github.com/jamiechurch/bobandjanedoe.git
cd bobandjanedoe
```

2. Create and activate a virtual environment:
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage - Regenerating Documents

All three generator scripts will create PDFs in the `bank_statements/` directory.

### Generate Checking Account Statements

```bash
python generate_statements.py
```

This will generate:
- 12 monthly checking account statements for 2024
- Realistic transaction patterns including income and expenses
- Running balance calculations

**Output**: `DoE_Statement_2024_XX_Month.pdf` (12 files)

### Generate Savings Account Statements

```bash
python generate_savings_statements.py
```

This will generate:
- 12 monthly savings account statements for 2024
- Monthly interest calculations at 4.25% APY
- Transfer tracking and occasional withdrawals

**Output**: `DoE_Savings_2024_XX_Month.pdf` (12 files)

### Generate Retirement Account Statements

```bash
python generate_retirement_statements.py
```

This will generate:
- Bob's 401(k) annual statement
- Jane's 403(b) annual statement
- Quarterly activity breakdowns
- Investment allocation details

**Output**:
- `Bob_Doe_401k_2024_Annual_Statement.pdf`
- `Jane_Doe_403b_2024_Annual_Statement.pdf`

### Generate All Documents

To regenerate all documents at once:

```bash
python generate_statements.py
python generate_savings_statements.py
python generate_retirement_statements.py
```

## Technical Details

### Generator Scripts

**generate_statements.py**
- Creates realistic checking account transactions
- Bi-monthly paycheck deposits (15th and end of month)
- Fixed monthly expenses (mortgage, insurance, loans)
- Variable expenses (utilities, groceries, gas, dining)
- Random transaction timing for realistic patterns
- Running balance calculations

**generate_savings_statements.py**
- Monthly $500 transfers from checking
- Interest calculation and accrual (4.25% APY monthly compounding)
- Random withdrawal events (~30% of months)
- Year-to-date interest tracking

**generate_retirement_statements.py**
- Annual statement generation for 401(k) and 403(b)
- Contribution calculations based on salary percentages
- Realistic investment return modeling (~10-12% for 2024)
- Investment allocation across multiple funds
- Quarterly activity breakdowns
- Fee calculations

### Dependencies

The project uses the following Python libraries:
- **fpdf2**: PDF generation library for creating realistic-looking documents
- **Standard library modules**: datetime, calendar, random, os

## Customization

You can modify the following parameters in the generator scripts:

### Checking Account (`generate_statements.py`)
- `BOB_NET_PAY` and `JANE_NET_PAY`: Bi-monthly net pay amounts
- `MONTHLY_EXPENSES`: Dictionary of fixed and variable expenses
- Starting balance and year

### Savings Account (`generate_savings_statements.py`)
- `ACCOUNT_INFO["apy"]`: Annual percentage yield (default: 4.25%)
- `MONTHLY_TRANSFER`: Amount transferred monthly from checking (default: $500)
- Starting balance

### Retirement Accounts (`generate_retirement_statements.py`)
- `BOB_401K` and `JANE_403B`: Comprehensive account information dictionaries
- Contribution percentages, salaries, and balances
- Investment return rates and fund allocations

## Important Notes

- All data in this project is **entirely fictional**
- SSNs use 000-00-XXXX format to indicate they are not real
- Bank routing numbers and account numbers are made up
- This is for **demonstration, testing, or educational purposes only**
- Do not use for fraud, identity theft, or any illegal purposes
- Generated statements include disclaimer footers

## Use Cases

This project can be used for:
- Software testing (financial applications, document processing)
- Educational demonstrations (personal finance, banking systems)
- UI/UX mockups requiring realistic financial documents
- Data pipeline testing for financial services
- Document parsing algorithm development

## License

This is a demonstration project. All data is fictional. Use responsibly.

## Author

Generated using Claude Code (claude.ai/code)
Repository: https://github.com/jamiechurch/bobandjanedoe
