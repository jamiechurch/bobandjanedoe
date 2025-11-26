#!/usr/bin/env python3
"""
Savings Account Statement Generator for Bob and Jane Doe
Generates 12 months of simulated savings account statements as PDF files
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
    "account_number": "****9821",
    "routing_number": "064000017",
    "account_type": "High-Yield Savings",
    "address": "456 Maple Street, Nashville, TN 37215",
    "apy": 4.25  # Annual Percentage Yield
}

# Monthly transfer from checking
MONTHLY_TRANSFER = 500.00


class SavingsStatement(FPDF):
    def __init__(self, month, year):
        super().__init__()
        self.month = month
        self.year = year
        self.month_name = datetime(year, month, 1).strftime("%B %Y")

    def header(self):
        # Bank logo area
        self.set_fill_color(0, 102, 51)  # Green for savings
        self.rect(0, 0, 210, 35, 'F')

        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 20)
        self.cell(0, 15, ACCOUNT_INFO["bank_name"], new_x="LMARGIN", new_y="NEXT", align='C')

        self.set_font('Helvetica', '', 10)
        self.cell(0, 8, "Member FDIC | Equal Housing Lender", new_x="LMARGIN", new_y="NEXT", align='C')

        self.ln(15)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-20)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 5, f"Page {self.page_no()}/{{nb}}", align='C', new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 5, "This is a simulated bank statement for demonstration purposes only.", align='C')

    def add_account_info(self, start_balance, end_balance, interest_earned):
        # Statement period
        _, last_day = monthrange(self.year, self.month)
        start_date = datetime(self.year, self.month, 1).strftime("%B %d, %Y")
        end_date = datetime(self.year, self.month, last_day).strftime("%B %d, %Y")

        self.set_font('Helvetica', 'B', 14)
        self.cell(0, 10, f"Savings Account Statement - {self.month_name}", new_x="LMARGIN", new_y="NEXT")

        self.set_font('Helvetica', '', 10)
        self.ln(3)

        # Two column layout for account info
        col_width = 95

        # Left column - Account holder info
        self.set_font('Helvetica', 'B', 10)
        self.cell(col_width, 6, "Account Holder:", new_x="RIGHT", new_y="TOP")
        self.cell(col_width, 6, "Account Details:", new_x="LMARGIN", new_y="NEXT")

        self.set_font('Helvetica', '', 10)
        self.cell(col_width, 5, ACCOUNT_INFO["account_holder"], new_x="RIGHT", new_y="TOP")
        self.cell(col_width, 5, f"Account Number: {ACCOUNT_INFO['account_number']}", new_x="LMARGIN", new_y="NEXT")

        self.cell(col_width, 5, ACCOUNT_INFO["address"], new_x="RIGHT", new_y="TOP")
        self.cell(col_width, 5, f"Account Type: {ACCOUNT_INFO['account_type']}", new_x="LMARGIN", new_y="NEXT")

        self.cell(col_width, 5, "", new_x="RIGHT", new_y="TOP")
        self.cell(col_width, 5, f"Statement Period: {start_date} - {end_date}", new_x="LMARGIN", new_y="NEXT")

        self.cell(col_width, 5, "", new_x="RIGHT", new_y="TOP")
        self.cell(col_width, 5, f"Annual Percentage Yield (APY): {ACCOUNT_INFO['apy']}%", new_x="LMARGIN", new_y="NEXT")

        self.ln(5)

        # Account Summary Box
        self.set_fill_color(232, 245, 233)  # Light green
        self.set_font('Helvetica', 'B', 11)
        self.cell(0, 8, "  Account Summary", new_x="LMARGIN", new_y="NEXT", fill=True)

        self.set_font('Helvetica', '', 10)
        summary_col = 47.5

        self.cell(summary_col, 7, f"  Beginning Balance:", border='L')
        self.cell(summary_col, 7, f"${start_balance:,.2f}", align='R')
        self.cell(summary_col, 7, f"  Ending Balance:", border=0)
        self.cell(summary_col, 7, f"${end_balance:,.2f}", align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        total_deposits = sum(t[2] for t in self.transactions if t[2] > 0)
        total_withdrawals = abs(sum(t[2] for t in self.transactions if t[2] < 0))

        self.cell(summary_col, 7, f"  Total Deposits:", border='L')
        self.cell(summary_col, 7, f"${total_deposits:,.2f}", align='R')
        self.cell(summary_col, 7, f"  Total Withdrawals:", border=0)
        self.cell(summary_col, 7, f"${total_withdrawals:,.2f}", align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        self.cell(summary_col, 7, f"  Interest Earned:", border='LB')
        self.cell(summary_col, 7, f"${interest_earned:,.2f}", align='R', border='B')
        self.cell(summary_col, 7, f"  YTD Interest:", border='B')
        self.cell(summary_col, 7, f"${self.ytd_interest:,.2f}", align='R', border='RB', new_x="LMARGIN", new_y="NEXT")

        self.ln(8)

    def add_transactions(self, transactions):
        self.transactions = transactions

        # Transaction header
        self.set_fill_color(0, 102, 51)
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 10)

        self.cell(25, 7, "Date", border=1, fill=True, align='C')
        self.cell(95, 7, "Description", border=1, fill=True, align='C')
        self.cell(35, 7, "Amount", border=1, fill=True, align='C')
        self.cell(35, 7, "Balance", border=1, fill=True, align='C', new_x="LMARGIN", new_y="NEXT")

        self.set_text_color(0, 0, 0)
        self.set_font('Helvetica', '', 9)

        # Sort transactions by date
        transactions.sort(key=lambda x: x[0])

        for i, (date, desc, amount, balance) in enumerate(transactions):
            # Alternate row colors
            if i % 2 == 0:
                self.set_fill_color(255, 255, 255)
            else:
                self.set_fill_color(245, 250, 245)

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
            self.cell(35, 6, f"${balance:,.2f}", border=1, fill=True, align='R', new_x="LMARGIN", new_y="NEXT")


def generate_savings_transactions(year, month, start_balance, ytd_interest):
    """Generate savings account transactions for a given month"""
    transactions = []
    _, last_day = monthrange(year, month)
    balance = start_balance

    # Transfer from checking (usually arrives between 16th-20th based on checking account)
    transfer_day = random.randint(16, 20)
    date = datetime(year, month, min(transfer_day, last_day))
    balance += MONTHLY_TRANSFER
    transactions.append((date, "Transfer from Checking ****4827", MONTHLY_TRANSFER, round(balance, 2)))

    # Calculate monthly interest (APY / 12)
    monthly_rate = ACCOUNT_INFO["apy"] / 100 / 12
    interest = round(start_balance * monthly_rate, 2)
    ytd_interest += interest

    # Interest posts on last day of month
    date = datetime(year, month, last_day)
    balance += interest
    transactions.append((date, "Interest Payment", interest, round(balance, 2)))

    # Occasional withdrawals for larger expenses (about 30% of months)
    if random.random() < 0.30:
        withdrawal_reasons = [
            ("Transfer to Checking - Car Repair", (200, 600)),
            ("Transfer to Checking - Medical", (150, 400)),
            ("Transfer to Checking - Home Repair", (300, 800)),
            ("Transfer to Checking - Holiday Shopping", (200, 500)),
            ("Transfer to Checking - Vacation", (400, 1000)),
        ]
        reason, amount_range = random.choice(withdrawal_reasons)
        amount = round(random.uniform(amount_range[0], amount_range[1]), 2)
        day = random.randint(5, last_day - 5)
        date = datetime(year, month, day)
        balance -= amount
        transactions.append((date, reason, -amount, round(balance, 2)))

    # Sort transactions by date and recalculate running balance
    transactions.sort(key=lambda x: x[0])

    balance = start_balance
    final_transactions = []
    for date, desc, amount, _ in transactions:
        balance = round(balance + amount, 2)
        final_transactions.append((date, desc, amount, balance))

    return final_transactions, balance, interest, ytd_interest


def main():
    # Create output directory
    output_dir = "bank_statements"
    os.makedirs(output_dir, exist_ok=True)

    # Starting balance (beginning of year)
    balance = 8500.00  # Starting savings account balance

    # Generate statements for 12 months (2024)
    year = 2024
    ytd_interest = 0.0

    print(f"Generating savings statements for {ACCOUNT_INFO['account_holder']}...")
    print("-" * 50)

    for month in range(1, 13):
        start_balance = balance

        # Generate transactions for this month
        transactions, end_balance, interest, ytd_interest = generate_savings_transactions(
            year, month, start_balance, ytd_interest
        )

        # Create PDF
        pdf = SavingsStatement(month, year)
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.transactions = transactions
        pdf.ytd_interest = ytd_interest
        pdf.add_account_info(start_balance, end_balance, interest)
        pdf.add_transactions(transactions)

        # Save PDF
        month_name = datetime(year, month, 1).strftime("%B")
        filename = f"{output_dir}/DoE_Savings_{year}_{month:02d}_{month_name}.pdf"
        pdf.output(filename)

        print(f"  {month_name} {year}: ${start_balance:,.2f} -> ${end_balance:,.2f} (Interest: ${interest:.2f})")

        # Carry forward the balance
        balance = end_balance

    print("-" * 50)
    print(f"Generated 12 savings statements in '{output_dir}/' directory")
    print(f"Final balance: ${balance:,.2f}")
    print(f"Total interest earned: ${ytd_interest:,.2f}")


if __name__ == "__main__":
    main()
