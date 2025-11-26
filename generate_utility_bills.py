#!/usr/bin/env python3
"""
Utility Bill Generator for Bob and Jane Doe
Generates 12 months of simulated utility bills (Electric, Gas, Water, Internet) as PDF files
"""

import os
import random
from datetime import datetime, timedelta
from calendar import monthrange
from fpdf import FPDF

# Customer Information
CUSTOMER_INFO = {
    "name": "Bob Doe & Jane Doe",
    "address": "456 Maple Street",
    "city_state_zip": "Nashville, TN 37215",
    "phone": "(615) 555-0123",
}

# Utility Company Information
UTILITIES = {
    "electric": {
        "company": "Nashville Electric Service",
        "account_number": "8429-3756-4821",
        "service_address": "456 Maple Street, Nashville, TN 37215",
        "amount_range": (140, 210),
        "bill_day_range": (15, 20),
        "usage_unit": "kWh",
        "rate_per_unit": 0.12,
        "base_charge": 18.50,
        "color": (0, 102, 204),  # Blue
        "phone": "1-888-NES-ELECTRIC",
    },
    "gas": {
        "company": "Piedmont Natural Gas",
        "account_number": "6912-4387-9021",
        "service_address": "456 Maple Street, Nashville, TN 37215",
        "amount_range": (45, 85),
        "bill_day_range": (18, 22),
        "usage_unit": "Therms",
        "rate_per_unit": 1.15,
        "base_charge": 12.00,
        "color": (255, 102, 0),  # Orange
        "phone": "1-800-752-7504",
    },
    "water": {
        "company": "Metro Water Services",
        "account_number": "4521-8936-7104",
        "service_address": "456 Maple Street, Nashville, TN 37215",
        "amount_range": (50, 65),
        "bill_day_range": (10, 15),
        "usage_unit": "CCF",
        "rate_per_unit": 4.82,
        "base_charge": 8.50,
        "color": (0, 153, 76),  # Green
        "phone": "(615) 862-4600",
    },
    "internet": {
        "company": "Comcast Xfinity",
        "account_number": "8482-9357-1046-2845",
        "service_address": "456 Maple Street, Nashville, TN 37215",
        "amount": 75.00,
        "bill_day": 8,
        "plan": "Xfinity Performance Pro+ (200 Mbps)",
        "color": (0, 0, 0),  # Black
        "phone": "1-800-COMCAST",
    }
}


class UtilityBill(FPDF):
    def __init__(self, utility_type, utility_info):
        super().__init__()
        self.utility_type = utility_type
        self.utility_info = utility_info

    def header(self):
        # Company header with color
        r, g, b = self.utility_info["color"]
        self.set_fill_color(r, g, b)
        self.rect(0, 0, 210, 30, 'F')

        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 18)
        self.cell(0, 12, self.utility_info["company"], ln=True, align='C')

        self.set_font('Helvetica', '', 10)
        self.cell(0, 8, f"Customer Service: {self.utility_info['phone']}", ln=True, align='C')

        self.ln(10)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-20)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 5, f"Page {self.page_no()}", align='C', ln=True)
        self.cell(0, 5, "This is a simulated utility bill for demonstration purposes only.", align='C')

    def add_bill_info(self, bill_date, due_date, amount, previous_balance=0.00):
        self.set_font('Helvetica', 'B', 14)
        self.cell(0, 10, "BILL STATEMENT", ln=True)
        self.ln(2)

        # Two column layout
        col_width = 95

        # Left column - Customer info
        self.set_font('Helvetica', 'B', 10)
        self.cell(col_width, 6, "CUSTOMER INFORMATION", ln=False)
        self.cell(col_width, 6, "ACCOUNT INFORMATION", ln=True)

        self.set_font('Helvetica', '', 9)
        self.cell(col_width, 5, CUSTOMER_INFO["name"], ln=False)
        self.cell(col_width, 5, f"Account Number: {self.utility_info['account_number']}", ln=True)

        self.cell(col_width, 5, CUSTOMER_INFO["address"], ln=False)
        self.cell(col_width, 5, f"Bill Date: {bill_date.strftime('%B %d, %Y')}", ln=True)

        self.cell(col_width, 5, CUSTOMER_INFO["city_state_zip"], ln=False)
        self.cell(col_width, 5, f"Due Date: {due_date.strftime('%B %d, %Y')}", ln=True)

        self.cell(col_width, 5, CUSTOMER_INFO["phone"], ln=False)
        self.cell(col_width, 5, f"Service Address:", ln=True)

        self.cell(col_width, 5, "", ln=False)
        self.cell(col_width, 5, f"  {self.utility_info['service_address']}", ln=True)

        self.ln(8)

        # Amount due box
        r, g, b = self.utility_info["color"]
        self.set_fill_color(r, g, b)
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 10, "  AMOUNT DUE", ln=True, fill=True)

        self.set_fill_color(240, 240, 240)
        self.set_text_color(0, 0, 0)
        self.set_font('Helvetica', '', 10)

        self.cell(95, 7, f"  Previous Balance:", fill=True)
        self.cell(95, 7, f"${previous_balance:.2f}", align='R', fill=True, ln=True)

        self.cell(95, 7, f"  Current Charges:", fill=True)
        self.cell(95, 7, f"${amount:.2f}", align='R', fill=True, ln=True)

        self.set_font('Helvetica', 'B', 11)
        self.cell(95, 8, f"  TOTAL AMOUNT DUE:", fill=True)
        self.cell(95, 8, f"${amount + previous_balance:.2f}", align='R', fill=True, ln=True)

        self.ln(8)


def generate_electric_bill(year, month):
    """Generate electric bill for a given month"""
    utility = UTILITIES["electric"]
    _, last_day = monthrange(year, month)

    # Bill date
    bill_day = random.randint(utility["bill_day_range"][0], min(utility["bill_day_range"][1], last_day))
    bill_date = datetime(year, month, bill_day)
    due_date = bill_date + timedelta(days=21)

    # Calculate usage
    base_usage = 950  # Base kWh per month
    # Seasonal variation (higher in summer and winter)
    if month in [6, 7, 8]:  # Summer AC usage
        usage = base_usage + random.randint(400, 800)
    elif month in [12, 1, 2]:  # Winter heating
        usage = base_usage + random.randint(200, 400)
    else:  # Spring/Fall
        usage = base_usage + random.randint(50, 200)

    # Calculate charges
    usage_charge = usage * utility["rate_per_unit"]
    base_charge = utility["base_charge"]
    total_amount = round(usage_charge + base_charge, 2)

    # Ensure amount is within expected range
    total_amount = max(utility["amount_range"][0], min(total_amount, utility["amount_range"][1]))

    # Create PDF
    pdf = UtilityBill("electric", utility)
    pdf.add_page()
    pdf.add_bill_info(bill_date, due_date, total_amount)

    # Usage details
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, "USAGE DETAILS", ln=True)

    # Billing period
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    prev_read_date = datetime(prev_year, prev_month, bill_day)

    pdf.set_font('Helvetica', '', 9)
    pdf.cell(0, 6, f"Billing Period: {prev_read_date.strftime('%m/%d/%Y')} - {bill_date.strftime('%m/%d/%Y')}", ln=True)
    pdf.cell(0, 6, f"Total Usage: {usage:,} {utility['usage_unit']}", ln=True)
    pdf.cell(0, 6, f"Average Daily Usage: {usage/30:.1f} {utility['usage_unit']}", ln=True)
    pdf.ln(6)

    # Charges breakdown
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, "CHARGES", ln=True)

    pdf.set_fill_color(248, 248, 248)
    pdf.set_font('Helvetica', '', 9)

    pdf.cell(130, 6, f"  Base Service Charge", fill=True)
    pdf.cell(60, 6, f"${base_charge:.2f}", align='R', fill=True, ln=True)

    pdf.cell(130, 6, f"  Energy Charge ({usage} {utility['usage_unit']} @ ${utility['rate_per_unit']:.4f})", fill=True)
    pdf.cell(60, 6, f"${usage_charge:.2f}", align='R', fill=True, ln=True)

    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(130, 7, f"  TOTAL CURRENT CHARGES", fill=True)
    pdf.cell(60, 7, f"${total_amount:.2f}", align='R', fill=True, ln=True)

    return pdf, total_amount, bill_date


def generate_gas_bill(year, month):
    """Generate gas bill for a given month"""
    utility = UTILITIES["gas"]
    _, last_day = monthrange(year, month)

    # Bill date
    bill_day = random.randint(utility["bill_day_range"][0], min(utility["bill_day_range"][1], last_day))
    bill_date = datetime(year, month, bill_day)
    due_date = bill_date + timedelta(days=21)

    # Calculate usage (higher in winter months)
    if month in [11, 12, 1, 2, 3]:  # Heating season
        usage = random.randint(45, 65)
    elif month in [6, 7, 8, 9]:  # Summer (minimal usage)
        usage = random.randint(8, 15)
    else:  # Shoulder seasons
        usage = random.randint(20, 35)

    # Calculate charges
    usage_charge = usage * utility["rate_per_unit"]
    base_charge = utility["base_charge"]
    total_amount = round(usage_charge + base_charge, 2)

    # Ensure amount is within expected range
    total_amount = max(utility["amount_range"][0], min(total_amount, utility["amount_range"][1]))

    # Create PDF
    pdf = UtilityBill("gas", utility)
    pdf.add_page()
    pdf.add_bill_info(bill_date, due_date, total_amount)

    # Usage details
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, "USAGE DETAILS", ln=True)

    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    prev_read_date = datetime(prev_year, prev_month, bill_day)

    pdf.set_font('Helvetica', '', 9)
    pdf.cell(0, 6, f"Billing Period: {prev_read_date.strftime('%m/%d/%Y')} - {bill_date.strftime('%m/%d/%Y')}", ln=True)
    pdf.cell(0, 6, f"Total Usage: {usage} {utility['usage_unit']}", ln=True)
    pdf.ln(6)

    # Charges breakdown
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, "CHARGES", ln=True)

    pdf.set_fill_color(248, 248, 248)
    pdf.set_font('Helvetica', '', 9)

    pdf.cell(130, 6, f"  Customer Charge", fill=True)
    pdf.cell(60, 6, f"${base_charge:.2f}", align='R', fill=True, ln=True)

    pdf.cell(130, 6, f"  Gas Supply ({usage} {utility['usage_unit']} @ ${utility['rate_per_unit']:.2f})", fill=True)
    pdf.cell(60, 6, f"${usage_charge:.2f}", align='R', fill=True, ln=True)

    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(130, 7, f"  TOTAL CURRENT CHARGES", fill=True)
    pdf.cell(60, 7, f"${total_amount:.2f}", align='R', fill=True, ln=True)

    return pdf, total_amount, bill_date


def generate_water_bill(year, month):
    """Generate water bill for a given month"""
    utility = UTILITIES["water"]
    _, last_day = monthrange(year, month)

    # Bill date
    bill_day = random.randint(utility["bill_day_range"][0], min(utility["bill_day_range"][1], last_day))
    bill_date = datetime(year, month, bill_day)
    due_date = bill_date + timedelta(days=21)

    # Calculate usage (CCF = hundred cubic feet)
    base_usage = 8  # Base CCF per month
    usage = base_usage + random.randint(0, 4)

    # Calculate charges
    usage_charge = usage * utility["rate_per_unit"]
    base_charge = utility["base_charge"]
    sewer_charge = usage * 5.20  # Sewer based on water usage
    total_amount = round(usage_charge + base_charge + sewer_charge, 2)

    # Ensure amount is within expected range
    total_amount = max(utility["amount_range"][0], min(total_amount, utility["amount_range"][1]))

    # Create PDF
    pdf = UtilityBill("water", utility)
    pdf.add_page()
    pdf.add_bill_info(bill_date, due_date, total_amount)

    # Usage details
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, "USAGE DETAILS", ln=True)

    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    prev_read_date = datetime(prev_year, prev_month, bill_day)

    pdf.set_font('Helvetica', '', 9)
    pdf.cell(0, 6, f"Billing Period: {prev_read_date.strftime('%m/%d/%Y')} - {bill_date.strftime('%m/%d/%Y')}", ln=True)
    pdf.cell(0, 6, f"Water Usage: {usage} {utility['usage_unit']} ({usage * 748} gallons)", ln=True)
    pdf.ln(6)

    # Charges breakdown
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, "CHARGES", ln=True)

    pdf.set_fill_color(248, 248, 248)
    pdf.set_font('Helvetica', '', 9)

    pdf.cell(130, 6, f"  Base Service Fee", fill=True)
    pdf.cell(60, 6, f"${base_charge:.2f}", align='R', fill=True, ln=True)

    pdf.cell(130, 6, f"  Water Usage ({usage} {utility['usage_unit']} @ ${utility['rate_per_unit']:.2f})", fill=True)
    pdf.cell(60, 6, f"${usage_charge:.2f}", align='R', fill=True, ln=True)

    pdf.cell(130, 6, f"  Sewer Charges ({usage} {utility['usage_unit']} @ $5.20)", fill=True)
    pdf.cell(60, 6, f"${sewer_charge:.2f}", align='R', fill=True, ln=True)

    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(130, 7, f"  TOTAL CURRENT CHARGES", fill=True)
    pdf.cell(60, 7, f"${total_amount:.2f}", align='R', fill=True, ln=True)

    return pdf, total_amount, bill_date


def generate_internet_bill(year, month):
    """Generate internet bill for a given month"""
    utility = UTILITIES["internet"]
    _, last_day = monthrange(year, month)

    # Bill date (fixed day)
    bill_day = min(utility["bill_day"], last_day)
    bill_date = datetime(year, month, bill_day)
    due_date = bill_date + timedelta(days=21)

    total_amount = utility["amount"]

    # Create PDF
    pdf = UtilityBill("internet", utility)
    pdf.add_page()
    pdf.add_bill_info(bill_date, due_date, total_amount)

    # Service details
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, "SERVICE DETAILS", ln=True)

    pdf.set_font('Helvetica', '', 9)
    pdf.cell(0, 6, f"Service Plan: {utility['plan']}", ln=True)
    pdf.cell(0, 6, f"Billing Cycle: {bill_date.strftime('%B %d, %Y')} - {(bill_date + timedelta(days=30)).strftime('%B %d, %Y')}", ln=True)
    pdf.ln(6)

    # Charges breakdown
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, "CHARGES", ln=True)

    pdf.set_fill_color(248, 248, 248)
    pdf.set_font('Helvetica', '', 9)

    pdf.cell(130, 6, f"  {utility['plan']}", fill=True)
    pdf.cell(60, 6, f"${total_amount:.2f}", align='R', fill=True, ln=True)

    pdf.cell(130, 6, f"  Equipment Rental (included)", fill=True)
    pdf.cell(60, 6, f"$0.00", align='R', fill=True, ln=True)

    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(130, 7, f"  TOTAL CURRENT CHARGES", fill=True)
    pdf.cell(60, 7, f"${total_amount:.2f}", align='R', fill=True, ln=True)

    # Add data usage note
    pdf.ln(8)
    pdf.set_font('Helvetica', 'I', 9)
    pdf.multi_cell(0, 5, "Data Usage: Your plan includes unlimited data with no overage charges.")

    return pdf, total_amount, bill_date


def main():
    # Create output directory
    output_dir = "bank_statements"
    os.makedirs(output_dir, exist_ok=True)

    year = 2024

    print(f"Generating utility bills for {CUSTOMER_INFO['name']}...")
    print("-" * 70)

    # Generate bills for each utility for 12 months
    for month in range(1, 13):
        month_name = datetime(year, month, 1).strftime("%B")

        # Electric bill
        pdf, amount, bill_date = generate_electric_bill(year, month)
        filename = f"{output_dir}/Electric_Bill_{year}_{month:02d}_{month_name}.pdf"
        pdf.output(filename)
        print(f"  {month_name} - Electric: ${amount:,.2f} (billed {bill_date.strftime('%m/%d/%Y')})")

        # Gas bill
        pdf, amount, bill_date = generate_gas_bill(year, month)
        filename = f"{output_dir}/Gas_Bill_{year}_{month:02d}_{month_name}.pdf"
        pdf.output(filename)
        print(f"  {month_name} - Gas:     ${amount:,.2f} (billed {bill_date.strftime('%m/%d/%Y')})")

        # Water bill
        pdf, amount, bill_date = generate_water_bill(year, month)
        filename = f"{output_dir}/Water_Bill_{year}_{month:02d}_{month_name}.pdf"
        pdf.output(filename)
        print(f"  {month_name} - Water:   ${amount:,.2f} (billed {bill_date.strftime('%m/%d/%Y')})")

        # Internet bill
        pdf, amount, bill_date = generate_internet_bill(year, month)
        filename = f"{output_dir}/Internet_Bill_{year}_{month:02d}_{month_name}.pdf"
        pdf.output(filename)
        print(f"  {month_name} - Internet: ${amount:.2f} (billed {bill_date.strftime('%m/%d/%Y')})")

        print()

    print("-" * 70)
    print(f"Generated 48 utility bills (4 types × 12 months) in '{output_dir}/' directory")


if __name__ == "__main__":
    main()
