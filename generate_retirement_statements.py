#!/usr/bin/env python3
"""
Retirement Account Statement Generator for Bob and Jane Doe
Generates annual 401(k) and 403(b) statements as PDF files
"""

import os
from datetime import datetime
from fpdf import FPDF

# Bob's 401(k) Information
BOB_401K = {
    "plan_name": "Acme Technology Corp 401(k) Plan",
    "administrator": "Fidelity Investments",
    "participant": "Bob Doe",
    "ssn_masked": "XXX-XX-0000",
    "dob": "March 15, 1977",
    "age": 47,
    "hire_date": "June 1, 2015",
    "address": "456 Maple Street, Nashville, TN 37215",
    "account_number": "Z4827-401K-0001",
    "annual_salary": 95000,
    "beginning_balance": 142500.00,  # Realistic for 47yo, ~1.5x salary (slightly behind)
    "employee_contribution_pct": 6.0,  # 6% of salary
    "employer_match_pct": 4.0,  # 4% match (50% of first 8%)
    "vesting_pct": 100,  # Fully vested after 9 years
}

# Jane's 403(b) Information
JANE_403B = {
    "plan_name": "Metro Nashville Public Schools 403(b) Plan",
    "administrator": "TIAA",
    "participant": "Jane Doe",
    "ssn_masked": "XXX-XX-0001",
    "dob": "August 22, 1979",
    "age": 45,
    "hire_date": "August 15, 2012",
    "address": "456 Maple Street, Nashville, TN 37215",
    "account_number": "T9821-403B-0001",
    "annual_salary": 65000,
    "beginning_balance": 98750.00,  # Realistic for 45yo teacher, ~1.5x salary
    "employee_contribution_pct": 8.0,  # 8% of salary (teachers often save more)
    "employer_match_pct": 3.0,  # 3% match
    "vesting_pct": 100,  # Fully vested
}


class RetirementStatement(FPDF):
    def __init__(self, account_type, account_info):
        super().__init__()
        self.account_type = account_type
        self.account_info = account_info

    def header(self):
        # Header with administrator branding
        if "Fidelity" in self.account_info["administrator"]:
            self.set_fill_color(0, 125, 50)  # Fidelity green
        else:
            self.set_fill_color(0, 51, 153)  # TIAA blue

        self.rect(0, 0, 210, 40, 'F')

        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 18)
        self.cell(0, 12, self.account_info["administrator"], new_x="LMARGIN", new_y="NEXT", align='C')

        self.set_font('Helvetica', '', 12)
        self.cell(0, 8, self.account_info["plan_name"], new_x="LMARGIN", new_y="NEXT", align='C')

        self.set_font('Helvetica', '', 10)
        self.cell(0, 8, f"Annual {self.account_type} Statement - Year Ending December 31, 2024", new_x="LMARGIN", new_y="NEXT", align='C')

        self.ln(12)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-25)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 4, "This is a simulated retirement account statement for demonstration purposes only.", align='C', new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 4, "Past performance does not guarantee future results. Investments are subject to market risk.", align='C', new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 4, f"Page {self.page_no()}/{{nb}}", align='C')

    def add_participant_info(self):
        info = self.account_info

        # Participant Information Box
        self.set_fill_color(245, 245, 245)
        self.set_font('Helvetica', 'B', 11)
        self.cell(0, 8, "  Participant Information", new_x="LMARGIN", new_y="NEXT", fill=True)

        self.set_font('Helvetica', '', 10)
        col_width = 95

        self.cell(col_width, 6, f"  Name: {info['participant']}", new_x="RIGHT", new_y="TOP")
        self.cell(col_width, 6, f"Account Number: {info['account_number']}", new_x="LMARGIN", new_y="NEXT")

        self.cell(col_width, 6, f"  SSN: {info['ssn_masked']}", new_x="RIGHT", new_y="TOP")
        self.cell(col_width, 6, f"Date of Birth: {info['dob']}", new_x="LMARGIN", new_y="NEXT")

        self.cell(col_width, 6, f"  Address: {info['address']}", new_x="RIGHT", new_y="TOP")
        self.cell(col_width, 6, f"Hire Date: {info['hire_date']}", new_x="LMARGIN", new_y="NEXT")

        self.ln(5)

    def add_account_summary(self, summary_data):
        info = self.account_info

        # Account Summary Box
        if "Fidelity" in info["administrator"]:
            self.set_fill_color(232, 245, 233)
        else:
            self.set_fill_color(232, 240, 254)

        self.set_font('Helvetica', 'B', 11)
        self.cell(0, 8, "  Account Summary", new_x="LMARGIN", new_y="NEXT", fill=True)

        self.set_font('Helvetica', '', 10)

        # Beginning and ending balance
        self.cell(95, 7, f"  Beginning Balance (01/01/2024):", border='L')
        self.cell(95, 7, f"${summary_data['beginning_balance']:,.2f}", align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        self.cell(95, 7, f"  Your Contributions:", border='L')
        self.cell(95, 7, f"+${summary_data['employee_contrib']:,.2f}", align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        self.cell(95, 7, f"  Employer Contributions:", border='L')
        self.cell(95, 7, f"+${summary_data['employer_contrib']:,.2f}", align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        self.cell(95, 7, f"  Investment Gains/(Losses):", border='L')
        gain_str = f"+${summary_data['investment_gain']:,.2f}" if summary_data['investment_gain'] >= 0 else f"-${abs(summary_data['investment_gain']):,.2f}"
        self.cell(95, 7, gain_str, align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        self.cell(95, 7, f"  Fees:", border='L')
        self.cell(95, 7, f"-${summary_data['fees']:,.2f}", align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        self.set_font('Helvetica', 'B', 10)
        self.cell(95, 8, f"  Ending Balance (12/31/2024):", border='LB')
        self.cell(95, 8, f"${summary_data['ending_balance']:,.2f}", align='R', border='RB', new_x="LMARGIN", new_y="NEXT")

        self.ln(3)

        # Year-over-year change
        change = summary_data['ending_balance'] - summary_data['beginning_balance']
        change_pct = (change / summary_data['beginning_balance']) * 100
        self.set_font('Helvetica', 'I', 9)
        self.cell(0, 6, f"  Total Change: ${change:,.2f} ({change_pct:+.1f}%)", new_x="LMARGIN", new_y="NEXT")

        self.ln(5)

    def add_contribution_summary(self, summary_data):
        info = self.account_info

        self.set_fill_color(245, 245, 245)
        self.set_font('Helvetica', 'B', 11)
        self.cell(0, 8, "  Contribution Details", new_x="LMARGIN", new_y="NEXT", fill=True)

        self.set_font('Helvetica', '', 10)

        self.cell(95, 6, f"  Annual Salary:", border='L')
        self.cell(95, 6, f"${info['annual_salary']:,.2f}", align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        self.cell(95, 6, f"  Your Contribution Rate:", border='L')
        self.cell(95, 6, f"{info['employee_contribution_pct']:.1f}%", align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        self.cell(95, 6, f"  Employer Match Rate:", border='L')
        self.cell(95, 6, f"{info['employer_match_pct']:.1f}%", align='R', border='R', new_x="LMARGIN", new_y="NEXT")

        self.cell(95, 6, f"  Vesting Percentage:", border='LB')
        self.cell(95, 6, f"{info['vesting_pct']}%", align='R', border='RB', new_x="LMARGIN", new_y="NEXT")

        self.ln(3)

        # IRS Limits reminder
        self.set_font('Helvetica', 'I', 8)
        if info['age'] >= 50:
            self.cell(0, 5, f"  2024 Contribution Limit: $23,000 + $7,500 catch-up (age 50+) = $30,500", new_x="LMARGIN", new_y="NEXT")
        else:
            self.cell(0, 5, f"  2024 Contribution Limit: $23,000 ($30,500 if age 50+)", new_x="LMARGIN", new_y="NEXT")

        self.ln(5)

    def add_investment_allocation(self, investments):
        self.set_fill_color(245, 245, 245)
        self.set_font('Helvetica', 'B', 11)
        self.cell(0, 8, "  Investment Holdings", new_x="LMARGIN", new_y="NEXT", fill=True)

        # Table header
        if "Fidelity" in self.account_info["administrator"]:
            self.set_fill_color(0, 125, 50)
        else:
            self.set_fill_color(0, 51, 153)
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 9)

        self.cell(75, 7, "Fund Name", border=1, fill=True, align='C')
        self.cell(25, 7, "Shares", border=1, fill=True, align='C')
        self.cell(30, 7, "Price", border=1, fill=True, align='C')
        self.cell(35, 7, "Value", border=1, fill=True, align='C')
        self.cell(25, 7, "% of Total", border=1, fill=True, align='C', new_x="LMARGIN", new_y="NEXT")

        self.set_text_color(0, 0, 0)
        self.set_font('Helvetica', '', 9)

        total_value = sum(inv['value'] for inv in investments)

        for i, inv in enumerate(investments):
            if i % 2 == 0:
                self.set_fill_color(255, 255, 255)
            else:
                self.set_fill_color(248, 248, 248)

            pct = (inv['value'] / total_value) * 100

            self.cell(75, 6, inv['name'][:35], border=1, fill=True)
            self.cell(25, 6, f"{inv['shares']:,.3f}", border=1, fill=True, align='R')
            self.cell(30, 6, f"${inv['price']:,.2f}", border=1, fill=True, align='R')
            self.cell(35, 6, f"${inv['value']:,.2f}", border=1, fill=True, align='R')
            self.cell(25, 6, f"{pct:.1f}%", border=1, fill=True, align='R', new_x="LMARGIN", new_y="NEXT")

        # Total row
        self.set_font('Helvetica', 'B', 9)
        self.set_fill_color(230, 230, 230)
        self.cell(130, 7, "Total", border=1, fill=True, align='R')
        self.cell(35, 7, f"${total_value:,.2f}", border=1, fill=True, align='R')
        self.cell(25, 7, "100.0%", border=1, fill=True, align='R', new_x="LMARGIN", new_y="NEXT")

        self.ln(5)

    def add_quarterly_activity(self, quarters):
        self.set_fill_color(245, 245, 245)
        self.set_font('Helvetica', 'B', 11)
        self.cell(0, 8, "  Quarterly Activity Summary", new_x="LMARGIN", new_y="NEXT", fill=True)

        # Table header
        self.set_fill_color(128, 128, 128)
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 9)

        self.cell(30, 7, "Quarter", border=1, fill=True, align='C')
        self.cell(35, 7, "Your Contrib", border=1, fill=True, align='C')
        self.cell(35, 7, "Employer", border=1, fill=True, align='C')
        self.cell(40, 7, "Invest Gain/Loss", border=1, fill=True, align='C')
        self.cell(50, 7, "Ending Balance", border=1, fill=True, align='C', new_x="LMARGIN", new_y="NEXT")

        self.set_text_color(0, 0, 0)
        self.set_font('Helvetica', '', 9)

        for i, q in enumerate(quarters):
            if i % 2 == 0:
                self.set_fill_color(255, 255, 255)
            else:
                self.set_fill_color(248, 248, 248)

            gain_str = f"${q['gain']:,.2f}" if q['gain'] >= 0 else f"-${abs(q['gain']):,.2f}"

            self.cell(30, 6, q['name'], border=1, fill=True, align='C')
            self.cell(35, 6, f"${q['employee']:,.2f}", border=1, fill=True, align='R')
            self.cell(35, 6, f"${q['employer']:,.2f}", border=1, fill=True, align='R')

            if q['gain'] >= 0:
                self.set_text_color(0, 100, 0)
            else:
                self.set_text_color(180, 0, 0)
            self.cell(40, 6, gain_str, border=1, fill=True, align='R')

            self.set_text_color(0, 0, 0)
            self.cell(50, 6, f"${q['balance']:,.2f}", border=1, fill=True, align='R', new_x="LMARGIN", new_y="NEXT")

        self.ln(5)

    def add_beneficiary_info(self, beneficiaries):
        self.set_fill_color(245, 245, 245)
        self.set_font('Helvetica', 'B', 11)
        self.cell(0, 8, "  Designated Beneficiaries", new_x="LMARGIN", new_y="NEXT", fill=True)

        self.set_font('Helvetica', '', 10)

        for ben in beneficiaries:
            self.cell(0, 6, f"  {ben['type']}: {ben['name']} ({ben['relationship']}) - {ben['percentage']}%", new_x="LMARGIN", new_y="NEXT")

        self.ln(3)


def generate_bob_401k():
    """Generate Bob's 401(k) statement"""
    info = BOB_401K

    # Calculate contributions
    employee_contrib = info['annual_salary'] * (info['employee_contribution_pct'] / 100)
    employer_contrib = info['annual_salary'] * (info['employer_match_pct'] / 100)

    # Simulate 2024 market returns (~12% for S&P 500 style returns)
    # Investment gain calculated on average balance throughout year
    avg_balance = info['beginning_balance'] + (employee_contrib + employer_contrib) / 2
    investment_return_rate = 0.118  # 11.8% return for 2024
    investment_gain = round(avg_balance * investment_return_rate, 2)

    fees = round(info['beginning_balance'] * 0.0015, 2)  # 0.15% annual fee

    ending_balance = round(
        info['beginning_balance'] +
        employee_contrib +
        employer_contrib +
        investment_gain -
        fees, 2
    )

    summary_data = {
        'beginning_balance': info['beginning_balance'],
        'employee_contrib': employee_contrib,
        'employer_contrib': employer_contrib,
        'investment_gain': investment_gain,
        'fees': fees,
        'ending_balance': ending_balance
    }

    # Investment allocation (target date fund heavy, typical for employer plan)
    investments = [
        {'name': 'Fidelity Freedom 2045 Fund', 'shares': 892.45, 'price': 15.82, 'value': ending_balance * 0.60},
        {'name': 'Fidelity 500 Index Fund', 'shares': 156.32, 'price': 178.45, 'value': ending_balance * 0.20},
        {'name': 'Fidelity Total Bond Index', 'shares': 523.18, 'price': 10.25, 'value': ending_balance * 0.10},
        {'name': 'Fidelity International Index', 'shares': 298.76, 'price': 12.34, 'value': ending_balance * 0.07},
        {'name': 'Fidelity Money Market', 'shares': ending_balance * 0.03, 'price': 1.00, 'value': ending_balance * 0.03},
    ]

    # Recalculate shares based on values
    for inv in investments:
        inv['shares'] = round(inv['value'] / inv['price'], 3)
        inv['value'] = round(inv['value'], 2)

    # Quarterly breakdown
    q1_emp = employee_contrib / 4
    q1_er = employer_contrib / 4
    q1_gain = round(info['beginning_balance'] * 0.028, 2)  # Q1 ~2.8%
    q1_bal = round(info['beginning_balance'] + q1_emp + q1_er + q1_gain, 2)

    q2_gain = round(q1_bal * 0.032, 2)  # Q2 ~3.2%
    q2_bal = round(q1_bal + q1_emp + q1_er + q2_gain, 2)

    q3_gain = round(q2_bal * 0.015, 2)  # Q3 ~1.5%
    q3_bal = round(q2_bal + q1_emp + q1_er + q3_gain, 2)

    q4_gain = round(ending_balance - q3_bal - q1_emp - q1_er, 2)  # Remainder

    quarters = [
        {'name': 'Q1 2024', 'employee': q1_emp, 'employer': q1_er, 'gain': q1_gain, 'balance': q1_bal},
        {'name': 'Q2 2024', 'employee': q1_emp, 'employer': q1_er, 'gain': q2_gain, 'balance': q2_bal},
        {'name': 'Q3 2024', 'employee': q1_emp, 'employer': q1_er, 'gain': q3_gain, 'balance': q3_bal},
        {'name': 'Q4 2024', 'employee': q1_emp, 'employer': q1_er, 'gain': q4_gain, 'balance': ending_balance},
    ]

    beneficiaries = [
        {'type': 'Primary', 'name': 'Jane Doe', 'relationship': 'Spouse', 'percentage': 100},
    ]

    return summary_data, investments, quarters, beneficiaries


def generate_jane_403b():
    """Generate Jane's 403(b) statement"""
    info = JANE_403B

    # Calculate contributions
    employee_contrib = info['annual_salary'] * (info['employee_contribution_pct'] / 100)
    employer_contrib = info['annual_salary'] * (info['employer_match_pct'] / 100)

    # Simulate 2024 market returns
    avg_balance = info['beginning_balance'] + (employee_contrib + employer_contrib) / 2
    investment_return_rate = 0.105  # 10.5% return (slightly more conservative allocation)
    investment_gain = round(avg_balance * investment_return_rate, 2)

    fees = round(info['beginning_balance'] * 0.0020, 2)  # 0.20% annual fee (TIAA slightly higher)

    ending_balance = round(
        info['beginning_balance'] +
        employee_contrib +
        employer_contrib +
        investment_gain -
        fees, 2
    )

    summary_data = {
        'beginning_balance': info['beginning_balance'],
        'employee_contrib': employee_contrib,
        'employer_contrib': employer_contrib,
        'investment_gain': investment_gain,
        'fees': fees,
        'ending_balance': ending_balance
    }

    # Investment allocation (TIAA typical funds)
    investments = [
        {'name': 'TIAA-CREF Lifecycle 2045 Fund', 'shares': 4521.33, 'price': 14.25, 'value': ending_balance * 0.50},
        {'name': 'TIAA-CREF Equity Index Fund', 'shares': 892.15, 'price': 32.18, 'value': ending_balance * 0.20},
        {'name': 'TIAA Traditional Annuity', 'shares': 1.00, 'price': ending_balance * 0.15, 'value': ending_balance * 0.15},
        {'name': 'TIAA-CREF Bond Index Fund', 'shares': 1245.67, 'price': 9.87, 'value': ending_balance * 0.10},
        {'name': 'TIAA-CREF International Equity', 'shares': 387.22, 'price': 18.45, 'value': ending_balance * 0.05},
    ]

    # Recalculate shares based on values
    for inv in investments:
        if inv['name'] != 'TIAA Traditional Annuity':
            inv['shares'] = round(inv['value'] / inv['price'], 3)
        inv['value'] = round(inv['value'], 2)

    # Quarterly breakdown
    q1_emp = employee_contrib / 4
    q1_er = employer_contrib / 4
    q1_gain = round(info['beginning_balance'] * 0.025, 2)
    q1_bal = round(info['beginning_balance'] + q1_emp + q1_er + q1_gain, 2)

    q2_gain = round(q1_bal * 0.030, 2)
    q2_bal = round(q1_bal + q1_emp + q1_er + q2_gain, 2)

    q3_gain = round(q2_bal * 0.012, 2)
    q3_bal = round(q2_bal + q1_emp + q1_er + q3_gain, 2)

    q4_gain = round(ending_balance - q3_bal - q1_emp - q1_er, 2)

    quarters = [
        {'name': 'Q1 2024', 'employee': q1_emp, 'employer': q1_er, 'gain': q1_gain, 'balance': q1_bal},
        {'name': 'Q2 2024', 'employee': q1_emp, 'employer': q1_er, 'gain': q2_gain, 'balance': q2_bal},
        {'name': 'Q3 2024', 'employee': q1_emp, 'employer': q1_er, 'gain': q3_gain, 'balance': q3_bal},
        {'name': 'Q4 2024', 'employee': q1_emp, 'employer': q1_er, 'gain': q4_gain, 'balance': ending_balance},
    ]

    beneficiaries = [
        {'type': 'Primary', 'name': 'Bob Doe', 'relationship': 'Spouse', 'percentage': 100},
    ]

    return summary_data, investments, quarters, beneficiaries


def main():
    output_dir = "bank_statements"
    os.makedirs(output_dir, exist_ok=True)

    print("Generating retirement account statements...")
    print("-" * 50)

    # Generate Bob's 401(k)
    summary, investments, quarters, beneficiaries = generate_bob_401k()

    pdf = RetirementStatement("401(k)", BOB_401K)
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.add_participant_info()
    pdf.add_account_summary(summary)
    pdf.add_contribution_summary(summary)
    pdf.add_investment_allocation(investments)
    pdf.add_quarterly_activity(quarters)
    pdf.add_beneficiary_info(beneficiaries)

    filename = f"{output_dir}/Bob_Doe_401k_2024_Annual_Statement.pdf"
    pdf.output(filename)

    print(f"  Bob's 401(k):")
    print(f"    Beginning Balance: ${summary['beginning_balance']:,.2f}")
    print(f"    Employee Contrib:  ${summary['employee_contrib']:,.2f}")
    print(f"    Employer Match:    ${summary['employer_contrib']:,.2f}")
    print(f"    Investment Gain:   ${summary['investment_gain']:,.2f}")
    print(f"    Ending Balance:    ${summary['ending_balance']:,.2f}")
    print()

    # Generate Jane's 403(b)
    summary, investments, quarters, beneficiaries = generate_jane_403b()

    pdf = RetirementStatement("403(b)", JANE_403B)
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.add_participant_info()
    pdf.add_account_summary(summary)
    pdf.add_contribution_summary(summary)
    pdf.add_investment_allocation(investments)
    pdf.add_quarterly_activity(quarters)
    pdf.add_beneficiary_info(beneficiaries)

    filename = f"{output_dir}/Jane_Doe_403b_2024_Annual_Statement.pdf"
    pdf.output(filename)

    print(f"  Jane's 403(b):")
    print(f"    Beginning Balance: ${summary['beginning_balance']:,.2f}")
    print(f"    Employee Contrib:  ${summary['employee_contrib']:,.2f}")
    print(f"    Employer Match:    ${summary['employer_contrib']:,.2f}")
    print(f"    Investment Gain:   ${summary['investment_gain']:,.2f}")
    print(f"    Ending Balance:    ${summary['ending_balance']:,.2f}")

    print()
    print("-" * 50)
    print(f"Generated retirement statements in '{output_dir}/' directory")


if __name__ == "__main__":
    main()
