#!/usr/bin/env python3
"""
Bank Statement Generator for Bob and Jane Doe
Generates 12 months of simulated bank statements as PDF files
"""

import os
import random
from datetime import datetime, timedelta
from calendar import monthrange
from fpdf import FPDF

# Account Information
ACCOUNT_INFO = {
    "bank_name": "First National Bank of Nashville",
    "account_holder": "Bob Doe & Jane Doe",
    "account_number": "****4827",
    "routing_number": "064000017",
    "account_type": "Joint Checking",
    "address": "456 Maple Street, Nashville, TN 37215"
}

# Monthly income (net pay, bi-monthly)
BOB_NET_PAY = 2853.43  # Per pay period
JANE_NET_PAY = 1982.39  # Per pay period

# Monthly expenses template
MONTHLY_EXPENSES = {
    "fixed": [
        ("Mortgage w/Escrow - First TN Bank", 2215.27, 1),  # $375k @ 4%, 30yr + taxes/insurance
        ("Auto Insurance - State Farm", 233.00, 5),
        ("Life Insurance - Northwestern", 85.00, 10),
        ("Internet - Comcast", 75.00, 8),
        ("Cell Phone - Verizon", 140.00, 12),
        ("Health Insurance Premium", 350.00, 1),
        ("Ford Motor Credit - Auto Loan", 504.00, 15),
        ("Harley Davidson Financial", 385.00, 10),  # 2019 Harley
        ("Progressive MC Insurance", 75.00, 10),  # Motorcycle insurance
        ("Streaming - Netflix", 15.99, 7),
        ("Streaming - Hulu", 17.99, 7),
        ("Streaming - Disney+", 13.99, 12),
        ("Gym - Planet Fitness", 49.99, 3),
    ],
    "utilities": [
        ("Nashville Electric Service", (140, 210), (15, 20)),
        ("Piedmont Natural Gas", (45, 85), (18, 22)),
        ("Metro Water Services", (50, 65), (10, 15)),
    ],
    "groceries": [
        "Kroger",
        "Publix",
        "Whole Foods",
        "Trader Joe's",
        "Costco",
        "Walmart Grocery",
    ],
    "gas_stations": [
        "Shell Oil",
        "Exxon",
        "BP",
        "Mapco",
        "Speedway",
    ],
    "dining": [
        "Chick-fil-A",
        "Panera Bread",
        "Chipotle",
        "Olive Garden",
        "Cracker Barrel",
        "Starbucks",
        "McDonald's",
        "Wendy's",
        "Local Bistro",
        "DoorDash",
        "Uber Eats",
    ],
    "shopping": [
        "Amazon.com",
        "Target",
        "Walmart",
        "Home Depot",
        "Lowe's",
        "TJ Maxx",
        "Kohl's",
        "Best Buy",
    ],
    "other": [
        "CVS Pharmacy",
        "Walgreens",
        "Great Clips",
        "PetSmart",
        "Dollar General",
    ]
}


class BankStatement(FPDF):
    def __init__(self, month, year):
        super().__init__()
        self.month = month
        self.year = year
        self.month_name = datetime(year, month, 1).strftime("%B %Y")

    def header(self):
        # Bank logo area
        self.set_fill_color(0, 51, 102)
        self.rect(0, 0, 210, 35, 'F')

        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 20)
        self.cell(0, 15, ACCOUNT_INFO["bank_name"], ln=True, align='C')

        self.set_font('Helvetica', '', 10)
        self.cell(0, 8, "Member FDIC | Equal Housing Lender", ln=True, align='C')

        self.ln(15)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-20)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 5, f"Page {self.page_no()}/{{nb}}", align='C', ln=True)
        self.cell(0, 5, "This is a simulated bank statement for demonstration purposes only.", align='C')

    def add_account_info(self, start_balance, end_balance):
        # Statement period
        _, last_day = monthrange(self.year, self.month)
        start_date = datetime(self.year, self.month, 1).strftime("%B %d, %Y")
        end_date = datetime(self.year, self.month, last_day).strftime("%B %d, %Y")

        self.set_font('Helvetica', 'B', 14)
        self.cell(0, 10, f"Account Statement - {self.month_name}", ln=True)

        self.set_font('Helvetica', '', 10)
        self.ln(3)

        # Two column layout for account info
        col_width = 95

        # Left column - Account holder info
        self.set_font('Helvetica', 'B', 10)
        self.cell(col_width, 6, "Account Holder:", ln=False)
        self.cell(col_width, 6, "Account Details:", ln=True)

        self.set_font('Helvetica', '', 10)
        self.cell(col_width, 5, ACCOUNT_INFO["account_holder"], ln=False)
        self.cell(col_width, 5, f"Account Number: {ACCOUNT_INFO['account_number']}", ln=True)

        self.cell(col_width, 5, ACCOUNT_INFO["address"], ln=False)
        self.cell(col_width, 5, f"Account Type: {ACCOUNT_INFO['account_type']}", ln=True)

        self.cell(col_width, 5, "", ln=False)
        self.cell(col_width, 5, f"Statement Period: {start_date} - {end_date}", ln=True)

        self.ln(5)

        # Account Summary Box
        self.set_fill_color(240, 240, 240)
        self.set_font('Helvetica', 'B', 11)
        self.cell(0, 8, "  Account Summary", ln=True, fill=True)

        self.set_font('Helvetica', '', 10)
        summary_col = 47.5

        self.cell(summary_col, 7, f"  Beginning Balance:", border='L')
        self.cell(summary_col, 7, f"${start_balance:,.2f}", align='R')
        self.cell(summary_col, 7, f"  Ending Balance:", border=0)
        self.cell(summary_col, 7, f"${end_balance:,.2f}", align='R', border='R', ln=True)

        total_deposits = sum(t[2] for t in self.transactions if t[2] > 0)
        total_withdrawals = abs(sum(t[2] for t in self.transactions if t[2] < 0))

        self.cell(summary_col, 7, f"  Total Deposits:", border='LB')
        self.cell(summary_col, 7, f"${total_deposits:,.2f}", align='R', border='B')
        self.cell(summary_col, 7, f"  Total Withdrawals:", border='B')
        self.cell(summary_col, 7, f"${total_withdrawals:,.2f}", align='R', border='RB', ln=True)

        self.ln(8)

    def add_transactions(self, transactions):
        self.transactions = transactions

        # Transaction header
        self.set_fill_color(0, 51, 102)
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 10)

        self.cell(25, 7, "Date", border=1, fill=True, align='C')
        self.cell(95, 7, "Description", border=1, fill=True, align='C')
        self.cell(35, 7, "Amount", border=1, fill=True, align='C')
        self.cell(35, 7, "Balance", border=1, fill=True, align='C', ln=True)

        self.set_text_color(0, 0, 0)
        self.set_font('Helvetica', '', 9)

        # Sort transactions by date
        transactions.sort(key=lambda x: x[0])

        running_balance = transactions[0][3] if transactions else 0

        for i, (date, desc, amount, balance) in enumerate(transactions):
            # Alternate row colors
            if i % 2 == 0:
                self.set_fill_color(255, 255, 255)
            else:
                self.set_fill_color(248, 248, 248)

            date_str = date.strftime("%m/%d/%Y")

            # Truncate description if too long
            if len(desc) > 45:
                desc = desc[:42] + "..."

            # Color code amounts
            if amount >= 0:
                amount_str = f"${amount:,.2f}"
                self.set_text_color(0, 100, 0)
            else:
                amount_str = f"-${abs(amount):,.2f}"
                self.set_text_color(180, 0, 0)

            self.cell(25, 6, date_str, border=1, fill=True, align='C')
            self.set_text_color(0, 0, 0)
            self.cell(95, 6, desc, border=1, fill=True)

            if amount >= 0:
                self.set_text_color(0, 100, 0)
            else:
                self.set_text_color(180, 0, 0)
            self.cell(35, 6, amount_str, border=1, fill=True, align='R')

            self.set_text_color(0, 0, 0)
            self.cell(35, 6, f"${balance:,.2f}", border=1, fill=True, align='R', ln=True)

            # Check if we need a new page
            if self.get_y() > 260:
                self.add_page()
                # Re-add header row
                self.set_fill_color(0, 51, 102)
                self.set_text_color(255, 255, 255)
                self.set_font('Helvetica', 'B', 10)
                self.cell(25, 7, "Date", border=1, fill=True, align='C')
                self.cell(95, 7, "Description", border=1, fill=True, align='C')
                self.cell(35, 7, "Amount", border=1, fill=True, align='C')
                self.cell(35, 7, "Balance", border=1, fill=True, align='C', ln=True)
                self.set_text_color(0, 0, 0)
                self.set_font('Helvetica', '', 9)


def generate_transactions(year, month, start_balance):
    """Generate realistic transactions for a given month"""
    transactions = []
    _, last_day = monthrange(year, month)
    balance = start_balance

    # Pay days (15th and last day of month)
    pay_day_1 = 15
    pay_day_2 = last_day

    # Add paychecks
    date1 = datetime(year, month, pay_day_1)
    balance += BOB_NET_PAY
    transactions.append((date1, "Direct Deposit - ACME TECHNOLOGY CORP", BOB_NET_PAY, round(balance, 2)))

    balance += JANE_NET_PAY
    transactions.append((date1, "Direct Deposit - METRO NASHVILLE SCHOOLS", JANE_NET_PAY, round(balance, 2)))

    date2 = datetime(year, month, pay_day_2)
    balance += BOB_NET_PAY
    transactions.append((date2, "Direct Deposit - ACME TECHNOLOGY CORP", BOB_NET_PAY, round(balance, 2)))

    balance += JANE_NET_PAY
    transactions.append((date2, "Direct Deposit - METRO NASHVILLE SCHOOLS", JANE_NET_PAY, round(balance, 2)))

    # Add fixed monthly expenses
    for name, amount, day in MONTHLY_EXPENSES["fixed"]:
        if day > last_day:
            day = last_day
        date = datetime(year, month, day)
        balance -= amount
        transactions.append((date, name, -amount, round(balance, 2)))

    # Add utilities (variable amounts)
    for name, amount_range, day_range in MONTHLY_EXPENSES["utilities"]:
        amount = round(random.uniform(amount_range[0], amount_range[1]), 2)
        day = random.randint(day_range[0], min(day_range[1], last_day))
        date = datetime(year, month, day)
        balance -= amount
        transactions.append((date, name, -amount, round(balance, 2)))

    # Add grocery shopping (4-6 trips per month)
    num_grocery_trips = random.randint(4, 6)
    for _ in range(num_grocery_trips):
        store = random.choice(MONTHLY_EXPENSES["groceries"])
        amount = round(random.uniform(85, 220), 2)
        day = random.randint(1, last_day)
        date = datetime(year, month, day)
        balance -= amount
        transactions.append((date, f"POS Purchase - {store}", -amount, round(balance, 2)))

    # Add gas station visits (6-10 per month)
    num_gas_stops = random.randint(6, 10)
    for _ in range(num_gas_stops):
        station = random.choice(MONTHLY_EXPENSES["gas_stations"])
        amount = round(random.uniform(35, 75), 2)
        day = random.randint(1, last_day)
        date = datetime(year, month, day)
        balance -= amount
        transactions.append((date, f"POS Purchase - {station}", -amount, round(balance, 2)))

    # Add dining out (8-12 times per month)
    num_dining = random.randint(8, 12)
    for _ in range(num_dining):
        restaurant = random.choice(MONTHLY_EXPENSES["dining"])
        amount = round(random.uniform(12, 85), 2)
        day = random.randint(1, last_day)
        date = datetime(year, month, day)
        balance -= amount
        transactions.append((date, f"POS Purchase - {restaurant}", -amount, round(balance, 2)))

    # Add shopping (3-6 times per month)
    num_shopping = random.randint(3, 6)
    for _ in range(num_shopping):
        store = random.choice(MONTHLY_EXPENSES["shopping"])
        amount = round(random.uniform(25, 150), 2)
        day = random.randint(1, last_day)
        date = datetime(year, month, day)
        balance -= amount
        transactions.append((date, f"POS Purchase - {store}", -amount, round(balance, 2)))

    # Add other miscellaneous (2-4 times per month)
    num_other = random.randint(2, 4)
    for _ in range(num_other):
        vendor = random.choice(MONTHLY_EXPENSES["other"])
        amount = round(random.uniform(15, 60), 2)
        day = random.randint(1, last_day)
        date = datetime(year, month, day)
        balance -= amount
        transactions.append((date, f"POS Purchase - {vendor}", -amount, round(balance, 2)))

    # Add ATM withdrawals (1-3 per month)
    num_atm = random.randint(1, 3)
    for _ in range(num_atm):
        amount = random.choice([40, 60, 80, 100, 120])
        day = random.randint(1, last_day)
        date = datetime(year, month, day)
        balance -= amount
        transactions.append((date, "ATM Withdrawal - First National Bank", -float(amount), round(balance, 2)))

    # Add savings transfer (monthly)
    transfer_day = random.randint(16, 20)
    date = datetime(year, month, min(transfer_day, last_day))
    balance -= 500.00
    transactions.append((date, "Transfer to Savings ****9821", -500.00, round(balance, 2)))

    # Jane's DraftKings gambling (~$700/month limit, spread across multiple transactions)
    draftkings_total = 0
    target_amount = 700.00
    while draftkings_total < target_amount:
        remaining = target_amount - draftkings_total
        if remaining <= 25:
            amount = remaining
        else:
            amount = round(random.uniform(15, min(75, remaining)), 2)
        draftkings_total += amount
        day = random.randint(1, last_day)
        date = datetime(year, month, day)
        balance -= amount
        transactions.append((date, "DraftKings", -amount, round(balance, 2)))

    # Sort all transactions by date and recalculate running balance
    transactions.sort(key=lambda x: (x[0], -x[2]))  # Sort by date, deposits first

    balance = start_balance
    final_transactions = []
    for date, desc, amount, _ in transactions:
        balance = round(balance + amount, 2)
        final_transactions.append((date, desc, amount, balance))

    return final_transactions, balance


def main():
    # Create output directory
    output_dir = "bank_statements"
    os.makedirs(output_dir, exist_ok=True)

    # Starting balance (beginning of year)
    balance = 3500.00  # Starting checking account balance

    # Generate statements for 12 months (2024)
    year = 2024

    print(f"Generating bank statements for {ACCOUNT_INFO['account_holder']}...")
    print("-" * 50)

    for month in range(1, 13):
        start_balance = balance

        # Generate transactions for this month
        transactions, end_balance = generate_transactions(year, month, start_balance)

        # Create PDF
        pdf = BankStatement(month, year)
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.transactions = transactions
        pdf.add_account_info(start_balance, end_balance)
        pdf.add_transactions(transactions)

        # Save PDF
        month_name = datetime(year, month, 1).strftime("%B")
        filename = f"{output_dir}/DoE_Statement_{year}_{month:02d}_{month_name}.pdf"
        pdf.output(filename)

        print(f"  {month_name} {year}: Starting ${start_balance:,.2f} -> Ending ${end_balance:,.2f}")

        # Carry forward the balance
        balance = end_balance

    print("-" * 50)
    print(f"Generated 12 statements in '{output_dir}/' directory")
    print(f"Final balance: ${balance:,.2f}")


if __name__ == "__main__":
    main()
