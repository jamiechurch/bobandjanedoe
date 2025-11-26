#!/usr/bin/env python3
"""
Tax Return Generator for Bob and Jane Doe
Generates a simulated Form 1040 (Married Filing Jointly) for 2023
"""

import os
from fpdf import FPDF

# Taxpayer Information
TAXPAYERS = {
    "primary": {
        "name": "Bob Doe",
        "ssn": "000-00-0000",
        "occupation": "Security Guard",
        "dob": "03/15/1977",
    },
    "spouse": {
        "name": "Jane Doe",
        "ssn": "000-00-0001",
        "occupation": "Teacher",
        "dob": "08/22/1979",
    },
    "address": "456 Maple Street",
    "city_state_zip": "Nashville, TN 37215",
    "filing_status": "Married Filing Jointly",
}

# 2023 Tax Year Data
TAX_YEAR = 2023

# Income Information
INCOME = {
    "bob_w2_wages": 95000.00,
    "bob_w2_federal_withheld": 14250.00,
    "jane_w2_wages": 65000.00,
    "jane_w2_federal_withheld": 8450.00,
    "interest_income": 385.00,  # From savings account
    "dividend_income": 0.00,
}

# 2023 Tax Constants
TAX_CONSTANTS_2023 = {
    "standard_deduction_mfj": 27700.00,
    "brackets_mfj": [
        (22000, 0.10),
        (89450, 0.12),
        (190750, 0.22),
        (364200, 0.24),
        (462500, 0.32),
        (693750, 0.35),
        (float('inf'), 0.37),
    ],
}


def calculate_tax(taxable_income, brackets):
    """Calculate tax using 2023 MFJ brackets"""
    tax = 0
    prev_bracket = 0

    for bracket_limit, rate in brackets:
        if taxable_income <= prev_bracket:
            break
        taxable_in_bracket = min(taxable_income, bracket_limit) - prev_bracket
        tax += taxable_in_bracket * rate
        prev_bracket = bracket_limit

    return round(tax, 2)


class Form1040(FPDF):
    def __init__(self):
        super().__init__()
        self.tax_data = {}

    def header(self):
        # IRS Form header
        self.set_fill_color(255, 255, 255)
        self.set_draw_color(0, 0, 0)

        # Top border box
        self.set_font('Helvetica', 'B', 16)
        self.cell(140, 10, "Form 1040", border=0)
        self.cell(50, 10, f"{TAX_YEAR}", border=0, align='R', new_x="LMARGIN", new_y="NEXT")

        self.set_font('Helvetica', '', 10)
        self.cell(140, 5, "Department of the Treasury - Internal Revenue Service", border=0)
        self.cell(50, 5, "", new_x="LMARGIN", new_y="NEXT")

        self.set_font('Helvetica', 'B', 14)
        self.cell(0, 8, "U.S. Individual Income Tax Return", new_x="LMARGIN", new_y="NEXT", align='C')

        self.set_font('Helvetica', 'I', 9)
        self.cell(0, 5, "THIS IS A SIMULATED TAX RETURN FOR DEMONSTRATION PURPOSES ONLY",
                  new_x="LMARGIN", new_y="NEXT", align='C')

        self.ln(5)

    def footer(self):
        self.set_y(-20)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 4, "This is a simulated tax return for demonstration purposes only.",
                  align='C', new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 4, "Do not file this document with the IRS.", align='C', new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 4, f"Page {self.page_no()}/{{nb}}", align='C')

    def add_taxpayer_info(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 7, "  Filing Status and Taxpayer Information", fill=True, new_x="LMARGIN", new_y="NEXT")

        self.set_font('Helvetica', '', 9)

        # Filing status
        self.cell(50, 6, "Filing Status:")
        self.set_font('Helvetica', 'B', 9)
        self.cell(0, 6, f"[X] {TAXPAYERS['filing_status']}", new_x="LMARGIN", new_y="NEXT")

        self.ln(2)
        self.set_font('Helvetica', '', 9)

        # Primary taxpayer
        self.cell(95, 6, f"Your first name and middle initial: {TAXPAYERS['primary']['name']}", border='LTB')
        self.cell(95, 6, f"Your social security number: {TAXPAYERS['primary']['ssn']}", border='RTB', new_x="LMARGIN", new_y="NEXT")

        # Spouse
        self.cell(95, 6, f"Spouse's first name and middle initial: {TAXPAYERS['spouse']['name']}", border='LB')
        self.cell(95, 6, f"Spouse's social security number: {TAXPAYERS['spouse']['ssn']}", border='RB', new_x="LMARGIN", new_y="NEXT")

        # Address
        self.cell(190, 6, f"Home address: {TAXPAYERS['address']}", border='LRB', new_x="LMARGIN", new_y="NEXT")
        self.cell(190, 6, f"City, state, and ZIP: {TAXPAYERS['city_state_zip']}", border='LRB', new_x="LMARGIN", new_y="NEXT")

        self.ln(5)

    def add_income_section(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 7, "  Income", fill=True, new_x="LMARGIN", new_y="NEXT")

        self.set_font('Helvetica', '', 9)

        total_wages = INCOME['bob_w2_wages'] + INCOME['jane_w2_wages']
        total_interest = INCOME['interest_income']
        total_income = total_wages + total_interest

        self.tax_data['total_wages'] = total_wages
        self.tax_data['total_interest'] = total_interest
        self.tax_data['total_income'] = total_income

        lines = [
            ("1a", "Total amount from Form(s) W-2, box 1", total_wages),
            ("1b", "Household employee wages not reported on Form(s) W-2", 0),
            ("1c", "Tip income not reported on line 1a", 0),
            ("1d", "Medicaid waiver payments not reported on Form(s) W-2", 0),
            ("1e", "Taxable dependent care benefits from Form 2441, line 26", 0),
            ("1f", "Employer-provided adoption benefits from Form 8839, line 29", 0),
            ("1g", "Wages from Form 8919, line 6", 0),
            ("1h", "Other earned income", 0),
            ("1i", "Nontaxable combat pay election", 0),
            ("1z", "Add lines 1a through 1h", total_wages),
        ]

        for line_num, description, amount in lines:
            self.cell(15, 5, f"  {line_num}", border='L')
            self.cell(135, 5, description)
            self.cell(10, 5, f"{line_num}")
            if amount > 0:
                self.cell(30, 5, f"${amount:,.2f}", align='R', border='R', new_x="LMARGIN", new_y="NEXT")
            else:
                self.cell(30, 5, "", border='R', new_x="LMARGIN", new_y="NEXT")

        # Interest and dividends
        self.cell(15, 5, "  2a", border='L')
        self.cell(135, 5, "Tax-exempt interest")
        self.cell(10, 5, "2a")
        self.cell(30, 5, "", border='R', new_x="LMARGIN", new_y="NEXT")

        self.cell(15, 5, "  2b", border='L')
        self.cell(135, 5, "Taxable interest")
        self.cell(10, 5, "2b")
        self.cell(30, 5, f"${total_interest:,.2f}", align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        self.cell(15, 5, "  3a", border='L')
        self.cell(135, 5, "Qualified dividends")
        self.cell(10, 5, "3a")
        self.cell(30, 5, "", border='R', new_x="LMARGIN", new_y="NEXT")

        self.cell(15, 5, "  3b", border='L')
        self.cell(135, 5, "Ordinary dividends")
        self.cell(10, 5, "3b")
        self.cell(30, 5, "", border='R', new_x="LMARGIN", new_y="NEXT")

        # Skip to line 9 - Total income
        self.set_font('Helvetica', 'B', 9)
        self.cell(15, 6, "  9", border='LB')
        self.cell(135, 6, "Total income. Add lines 1z, 2b, 3b, 4b, 5b, 6b, 7, and 8", border='B')
        self.cell(10, 6, "9", border='B')
        self.cell(30, 6, f"${total_income:,.2f}", align='R', border='RB', new_x="LMARGIN", new_y="NEXT")

        self.ln(3)

    def add_adjustments_section(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 7, "  Adjustments to Income", fill=True, new_x="LMARGIN", new_y="NEXT")

        self.set_font('Helvetica', '', 9)

        # Common adjustments (most are 0 for this couple)
        self.cell(15, 5, "  10", border='L')
        self.cell(135, 5, "Adjustments to income from Schedule 1, line 26")
        self.cell(10, 5, "10")
        self.cell(30, 5, "$0.00", align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        agi = self.tax_data['total_income']
        self.tax_data['agi'] = agi

        self.set_font('Helvetica', 'B', 9)
        self.cell(15, 6, "  11", border='LB')
        self.cell(135, 6, "Adjusted gross income. Subtract line 10 from line 9", border='B')
        self.cell(10, 6, "11", border='B')
        self.cell(30, 6, f"${agi:,.2f}", align='R', border='RB', new_x="LMARGIN", new_y="NEXT")

        self.ln(3)

    def add_deductions_section(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 7, "  Tax and Credits", fill=True, new_x="LMARGIN", new_y="NEXT")

        self.set_font('Helvetica', '', 9)

        standard_ded = TAX_CONSTANTS_2023['standard_deduction_mfj']
        self.tax_data['standard_deduction'] = standard_ded

        self.cell(15, 5, "  12", border='L')
        self.cell(135, 5, f"Standard deduction or itemized deductions (from Schedule A)")
        self.cell(10, 5, "12")
        self.cell(30, 5, f"${standard_ded:,.2f}", align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        self.cell(15, 5, "  13", border='L')
        self.cell(135, 5, "Qualified business income deduction from Form 8995 or 8995-A")
        self.cell(10, 5, "13")
        self.cell(30, 5, "$0.00", align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        self.cell(15, 5, "  14", border='L')
        self.cell(135, 5, "Add lines 12 and 13")
        self.cell(10, 5, "14")
        self.cell(30, 5, f"${standard_ded:,.2f}", align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        taxable_income = max(0, self.tax_data['agi'] - standard_ded)
        self.tax_data['taxable_income'] = taxable_income

        self.set_font('Helvetica', 'B', 9)
        self.cell(15, 6, "  15", border='LB')
        self.cell(135, 6, "Taxable income. Subtract line 14 from line 11. If zero or less, enter -0-", border='B')
        self.cell(10, 6, "15", border='B')
        self.cell(30, 6, f"${taxable_income:,.2f}", align='R', border='RB', new_x="LMARGIN", new_y="NEXT")

        self.ln(3)

    def add_tax_computation(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 7, "  Tax Computation", fill=True, new_x="LMARGIN", new_y="NEXT")

        self.set_font('Helvetica', '', 9)

        tax = calculate_tax(self.tax_data['taxable_income'], TAX_CONSTANTS_2023['brackets_mfj'])
        self.tax_data['tax'] = tax

        self.cell(15, 5, "  16", border='L')
        self.cell(135, 5, "Tax (see instructions). Check if from: [ ] Form 8814 [ ] Form 4972 [ ] Other")
        self.cell(10, 5, "16")
        self.cell(30, 5, f"${tax:,.2f}", align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        self.cell(15, 5, "  17", border='L')
        self.cell(135, 5, "Amount from Schedule 2, line 3")
        self.cell(10, 5, "17")
        self.cell(30, 5, "$0.00", align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        self.cell(15, 5, "  18", border='L')
        self.cell(135, 5, "Add lines 16 and 17")
        self.cell(10, 5, "18")
        self.cell(30, 5, f"${tax:,.2f}", align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        # Credits
        self.cell(15, 5, "  19", border='L')
        self.cell(135, 5, "Child tax credit or credit for other dependents from Schedule 8812")
        self.cell(10, 5, "19")
        self.cell(30, 5, "$0.00", align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        self.cell(15, 5, "  20", border='L')
        self.cell(135, 5, "Amount from Schedule 3, line 8")
        self.cell(10, 5, "20")
        self.cell(30, 5, "$0.00", align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        self.cell(15, 5, "  21", border='L')
        self.cell(135, 5, "Add lines 19 and 20")
        self.cell(10, 5, "21")
        self.cell(30, 5, "$0.00", align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        self.set_font('Helvetica', 'B', 9)
        self.cell(15, 6, "  22", border='L')
        self.cell(135, 6, "Subtract line 21 from line 18. If zero or less, enter -0-")
        self.cell(10, 6, "22")
        self.cell(30, 6, f"${tax:,.2f}", align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        self.cell(15, 6, "  23", border='L')
        self.cell(135, 6, "Other taxes, including self-employment tax, from Schedule 2, line 21")
        self.cell(10, 6, "23")
        self.cell(30, 6, "$0.00", align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        self.cell(15, 6, "  24", border='LB')
        self.cell(135, 6, "Total tax. Add lines 22 and 23", border='B')
        self.cell(10, 6, "24", border='B')
        self.cell(30, 6, f"${tax:,.2f}", align='R', border='RB', new_x="LMARGIN", new_y="NEXT")

        self.tax_data['total_tax'] = tax
        self.ln(3)

    def add_payments_section(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 7, "  Payments", fill=True, new_x="LMARGIN", new_y="NEXT")

        self.set_font('Helvetica', '', 9)

        total_withheld = INCOME['bob_w2_federal_withheld'] + INCOME['jane_w2_federal_withheld']
        self.tax_data['total_withheld'] = total_withheld

        self.cell(15, 5, "  25a", border='L')
        self.cell(135, 5, "Federal income tax withheld from Form(s) W-2")
        self.cell(10, 5, "25a")
        self.cell(30, 5, f"${total_withheld:,.2f}", align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        self.cell(15, 5, "  25b", border='L')
        self.cell(135, 5, "Federal income tax withheld from Form(s) 1099")
        self.cell(10, 5, "25b")
        self.cell(30, 5, "$0.00", align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        self.cell(15, 5, "  25c", border='L')
        self.cell(135, 5, "Other forms (see instructions)")
        self.cell(10, 5, "25c")
        self.cell(30, 5, "$0.00", align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        self.cell(15, 5, "  25d", border='L')
        self.cell(135, 5, "Add lines 25a through 25c")
        self.cell(10, 5, "25d")
        self.cell(30, 5, f"${total_withheld:,.2f}", align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        self.cell(15, 5, "  26", border='L')
        self.cell(135, 5, "2023 estimated tax payments and amount applied from 2022 return")
        self.cell(10, 5, "26")
        self.cell(30, 5, "$0.00", align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        # Earned Income Credit (they don't qualify due to income)
        self.cell(15, 5, "  27", border='L')
        self.cell(135, 5, "Earned income credit (EIC)")
        self.cell(10, 5, "27")
        self.cell(30, 5, "$0.00", align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        self.cell(15, 5, "  28", border='L')
        self.cell(135, 5, "Additional child tax credit from Schedule 8812")
        self.cell(10, 5, "28")
        self.cell(30, 5, "$0.00", align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        self.cell(15, 5, "  29", border='L')
        self.cell(135, 5, "American opportunity credit from Form 8863, line 8")
        self.cell(10, 5, "29")
        self.cell(30, 5, "$0.00", align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        self.cell(15, 5, "  31", border='L')
        self.cell(135, 5, "Amount from Schedule 3, line 15")
        self.cell(10, 5, "31")
        self.cell(30, 5, "$0.00", align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        self.set_font('Helvetica', 'B', 9)
        self.cell(15, 6, "  33", border='LB')
        self.cell(135, 6, "Total payments. Add lines 25d, 26, 27, 28, 29, 31, and 32", border='B')
        self.cell(10, 6, "33", border='B')
        self.cell(30, 6, f"${total_withheld:,.2f}", align='R', border='RB', new_x="LMARGIN", new_y="NEXT")

        self.tax_data['total_payments'] = total_withheld
        self.ln(3)

    def add_refund_section(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 7, "  Refund", fill=True, new_x="LMARGIN", new_y="NEXT")

        self.set_font('Helvetica', '', 9)

        total_payments = self.tax_data['total_payments']
        total_tax = self.tax_data['total_tax']

        if total_payments > total_tax:
            refund = total_payments - total_tax
            amount_owed = 0
        else:
            refund = 0
            amount_owed = total_tax - total_payments

        self.tax_data['refund'] = refund
        self.tax_data['amount_owed'] = amount_owed

        self.set_font('Helvetica', 'B', 9)
        self.cell(15, 6, "  34", border='L')
        self.cell(135, 6, "If line 33 is more than line 24, subtract line 24 from line 33. This is the amount OVERPAID")
        self.cell(10, 6, "34")
        self.cell(30, 6, f"${refund:,.2f}", align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        self.set_font('Helvetica', '', 9)
        self.cell(15, 5, "  35a", border='L')
        self.cell(135, 5, "Amount of line 34 you want REFUNDED TO YOU")
        self.cell(10, 5, "35a")
        self.cell(30, 5, f"${refund:,.2f}", align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        self.cell(15, 5, "  35b", border='L')
        self.cell(95, 5, "Routing number: 064000017")
        self.cell(40, 5, "Type: [X] Checking [ ] Savings")
        self.cell(10, 5, "")
        self.cell(30, 5, "", border='R', new_x="LMARGIN", new_y="NEXT")

        self.cell(15, 5, "  35d", border='LB')
        self.cell(135, 5, "Account number: ****4827", border='B')
        self.cell(10, 5, "", border='B')
        self.cell(30, 5, "", border='RB', new_x="LMARGIN", new_y="NEXT")

        self.ln(3)

        # Amount You Owe section
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 7, "  Amount You Owe", fill=True, new_x="LMARGIN", new_y="NEXT")

        self.set_font('Helvetica', '', 9)
        self.cell(15, 5, "  37", border='LB')
        self.cell(135, 5, "Amount you owe. Subtract line 33 from line 24", border='B')
        self.cell(10, 5, "37", border='B')
        self.cell(30, 5, f"${amount_owed:,.2f}", align='R', border='RB', new_x="LMARGIN", new_y="NEXT")

        self.ln(3)

    def add_signature_section(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 7, "  Sign Here (Joint return? Both must sign)", fill=True, new_x="LMARGIN", new_y="NEXT")

        self.set_font('Helvetica', '', 9)

        self.cell(95, 6, "  Your signature: Bob Doe", border='LB')
        self.cell(95, 6, "Date: 04/15/2024", border='RB', new_x="LMARGIN", new_y="NEXT")

        self.cell(95, 6, "  Spouse's signature: Jane Doe", border='LB')
        self.cell(95, 6, "Date: 04/15/2024", border='RB', new_x="LMARGIN", new_y="NEXT")

        self.cell(95, 6, f"  Your occupation: {TAXPAYERS['primary']['occupation']}", border='LB')
        self.cell(95, 6, f"Spouse's occupation: {TAXPAYERS['spouse']['occupation']}", border='RB', new_x="LMARGIN", new_y="NEXT")

        self.ln(5)

    def add_summary_page(self):
        """Add a summary page with tax calculation breakdown"""
        self.add_page()

        self.set_font('Helvetica', 'B', 14)
        self.cell(0, 10, "Tax Return Summary - For Reference Only", new_x="LMARGIN", new_y="NEXT", align='C')

        self.ln(5)

        self.set_font('Helvetica', 'B', 11)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 7, "  Income Summary", fill=True, new_x="LMARGIN", new_y="NEXT")

        self.set_font('Helvetica', '', 10)

        self.cell(120, 6, f"  Bob Doe - W-2 Wages (Acme Technology Corp)")
        self.cell(70, 6, f"${INCOME['bob_w2_wages']:,.2f}", align='R', new_x="LMARGIN", new_y="NEXT")

        self.cell(120, 6, f"  Jane Doe - W-2 Wages (Metro Nashville Public Schools)")
        self.cell(70, 6, f"${INCOME['jane_w2_wages']:,.2f}", align='R', new_x="LMARGIN", new_y="NEXT")

        self.cell(120, 6, f"  Interest Income (Savings Account)")
        self.cell(70, 6, f"${INCOME['interest_income']:,.2f}", align='R', new_x="LMARGIN", new_y="NEXT")

        self.set_font('Helvetica', 'B', 10)
        self.cell(120, 7, f"  Total Income")
        self.cell(70, 7, f"${self.tax_data['total_income']:,.2f}", align='R', new_x="LMARGIN", new_y="NEXT")

        self.ln(3)

        # Deductions
        self.set_font('Helvetica', 'B', 11)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 7, "  Deductions", fill=True, new_x="LMARGIN", new_y="NEXT")

        self.set_font('Helvetica', '', 10)
        self.cell(120, 6, f"  Standard Deduction (Married Filing Jointly)")
        self.cell(70, 6, f"-${self.tax_data['standard_deduction']:,.2f}", align='R', new_x="LMARGIN", new_y="NEXT")

        self.set_font('Helvetica', 'B', 10)
        self.cell(120, 7, f"  Taxable Income")
        self.cell(70, 7, f"${self.tax_data['taxable_income']:,.2f}", align='R', new_x="LMARGIN", new_y="NEXT")

        self.ln(3)

        # Tax Calculation Breakdown
        self.set_font('Helvetica', 'B', 11)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 7, "  2023 Tax Calculation (Married Filing Jointly Brackets)", fill=True, new_x="LMARGIN", new_y="NEXT")

        self.set_font('Helvetica', '', 10)

        taxable = self.tax_data['taxable_income']

        # 10% bracket
        bracket_10 = min(taxable, 22000)
        tax_10 = bracket_10 * 0.10
        self.cell(120, 6, f"  10% on first $22,000")
        self.cell(70, 6, f"${tax_10:,.2f}", align='R', new_x="LMARGIN", new_y="NEXT")

        # 12% bracket
        bracket_12 = min(max(0, taxable - 22000), 89450 - 22000)
        tax_12 = bracket_12 * 0.12
        self.cell(120, 6, f"  12% on $22,001 - $89,450 (${bracket_12:,.0f})")
        self.cell(70, 6, f"${tax_12:,.2f}", align='R', new_x="LMARGIN", new_y="NEXT")

        # 22% bracket
        bracket_22 = min(max(0, taxable - 89450), 190750 - 89450)
        tax_22 = bracket_22 * 0.22
        self.cell(120, 6, f"  22% on $89,451 - $190,750 (${bracket_22:,.0f})")
        self.cell(70, 6, f"${tax_22:,.2f}", align='R', new_x="LMARGIN", new_y="NEXT")

        self.set_font('Helvetica', 'B', 10)
        self.cell(120, 7, f"  Total Federal Tax")
        self.cell(70, 7, f"${self.tax_data['total_tax']:,.2f}", align='R', new_x="LMARGIN", new_y="NEXT")

        self.ln(3)

        # Withholdings
        self.set_font('Helvetica', 'B', 11)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 7, "  Tax Payments (Withholdings)", fill=True, new_x="LMARGIN", new_y="NEXT")

        self.set_font('Helvetica', '', 10)
        self.cell(120, 6, f"  Bob Doe - Federal Tax Withheld")
        self.cell(70, 6, f"${INCOME['bob_w2_federal_withheld']:,.2f}", align='R', new_x="LMARGIN", new_y="NEXT")

        self.cell(120, 6, f"  Jane Doe - Federal Tax Withheld")
        self.cell(70, 6, f"${INCOME['jane_w2_federal_withheld']:,.2f}", align='R', new_x="LMARGIN", new_y="NEXT")

        self.set_font('Helvetica', 'B', 10)
        self.cell(120, 7, f"  Total Payments")
        self.cell(70, 7, f"${self.tax_data['total_payments']:,.2f}", align='R', new_x="LMARGIN", new_y="NEXT")

        self.ln(3)

        # Final Result
        self.set_font('Helvetica', 'B', 11)
        if self.tax_data['refund'] > 0:
            self.set_fill_color(200, 250, 200)
            self.cell(0, 7, "  REFUND DUE", fill=True, new_x="LMARGIN", new_y="NEXT")
        else:
            self.set_fill_color(250, 200, 200)
            self.cell(0, 7, "  AMOUNT OWED", fill=True, new_x="LMARGIN", new_y="NEXT")

        self.set_font('Helvetica', '', 10)
        self.cell(120, 6, f"  Total Tax Liability")
        self.cell(70, 6, f"${self.tax_data['total_tax']:,.2f}", align='R', new_x="LMARGIN", new_y="NEXT")

        self.cell(120, 6, f"  Total Payments")
        self.cell(70, 6, f"-${self.tax_data['total_payments']:,.2f}", align='R', new_x="LMARGIN", new_y="NEXT")

        self.set_font('Helvetica', 'B', 12)
        if self.tax_data['refund'] > 0:
            self.set_text_color(0, 100, 0)
            self.cell(120, 8, f"  REFUND AMOUNT")
            self.cell(70, 8, f"${self.tax_data['refund']:,.2f}", align='R', new_x="LMARGIN", new_y="NEXT")
        else:
            self.set_text_color(180, 0, 0)
            self.cell(120, 8, f"  AMOUNT OWED")
            self.cell(70, 8, f"${self.tax_data['amount_owed']:,.2f}", align='R', new_x="LMARGIN", new_y="NEXT")

        self.set_text_color(0, 0, 0)

        self.ln(5)

        # Effective tax rate
        self.set_font('Helvetica', 'I', 9)
        effective_rate = (self.tax_data['total_tax'] / self.tax_data['total_income']) * 100
        marginal_rate = 22  # They're in the 22% bracket
        self.cell(0, 5, f"Effective Tax Rate: {effective_rate:.1f}% | Marginal Tax Rate: {marginal_rate}%",
                  align='C', new_x="LMARGIN", new_y="NEXT")


def main():
    output_dir = "bank_statements"
    os.makedirs(output_dir, exist_ok=True)

    print("Generating 2023 Tax Return for Bob and Jane Doe...")
    print("-" * 50)

    pdf = Form1040()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.add_taxpayer_info()
    pdf.add_income_section()
    pdf.add_adjustments_section()
    pdf.add_deductions_section()
    pdf.add_tax_computation()
    pdf.add_payments_section()
    pdf.add_refund_section()
    pdf.add_signature_section()
    pdf.add_summary_page()

    filename = f"{output_dir}/Doe_Form1040_{TAX_YEAR}_Tax_Return.pdf"
    pdf.output(filename)

    print(f"  Filing Status: Married Filing Jointly")
    print(f"  Total Income: ${pdf.tax_data['total_income']:,.2f}")
    print(f"  Standard Deduction: ${pdf.tax_data['standard_deduction']:,.2f}")
    print(f"  Taxable Income: ${pdf.tax_data['taxable_income']:,.2f}")
    print(f"  Total Tax: ${pdf.tax_data['total_tax']:,.2f}")
    print(f"  Total Withheld: ${pdf.tax_data['total_payments']:,.2f}")

    if pdf.tax_data['refund'] > 0:
        print(f"  REFUND: ${pdf.tax_data['refund']:,.2f}")
    else:
        print(f"  AMOUNT OWED: ${pdf.tax_data['amount_owed']:,.2f}")

    print("-" * 50)
    print(f"Generated tax return: {filename}")


if __name__ == "__main__":
    main()
