# Financial Analysis Agents - Setup Guide

This guide provides step-by-step instructions for setting up and using the 8 financial analysis agents defined in `agents.txt` to analyze the Bob and Jane Doe financial documents.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Setup for Claude Code](#setup-for-claude-code)
3. [Setup for ChatGPT/OpenAI](#setup-for-chatgpt)
4. [Setup for Google Gemini](#setup-for-google-gemini)
5. [Setup for Other AI Systems](#setup-for-other-ai-systems)
6. [Running Agent Analysis](#running-agent-analysis)
7. [Troubleshooting](#troubleshooting)

---

## Quick Start

**What you need:**
- The `statements/` directory with all generated PDFs (74 files total)
- An AI assistant that can read PDF files
- The agent definitions from `agents.txt`

**Recommended order to run agents:**
1. Document Completeness Checker (verify all files present)
2. Financial Auditor (verify accuracy)
3. Spending Pattern Analyzer (understand spending habits)
4. Cash Flow Analyst (identify cash flow issues)
5. Budget Compliance Monitor (assess budget health)
6. Savings Goal Tracker (track savings progress)
7. Retirement Account Analyzer (analyze retirement savings)
8. Tax Document Verifier (verify tax return)

---

## Setup for Claude Code

Claude Code supports custom agents through the `.claude/agents/` directory.

### Step 1: Create Agent Directory

```bash
mkdir -p .claude/agents
```

### Step 2: Create Individual Agent Files

For each agent in `agents.txt`, create a markdown file in `.claude/agents/`:

**Example: Financial Auditor**

Create `.claude/agents/financial-auditor.md`:

```markdown
You are a financial auditor. Review all documents in the statements/ directory and verify that:

1. Utility bill amounts match the corresponding charges in bank statements
2. All running balances are calculated correctly
3. Monthly transfers to savings appear in both checking and savings statements
4. All dates and amounts are consistent across documents
5. Interest calculations in savings statements are accurate

Report any discrepancies or errors found.

When analyzing:
- Read PDFs from the statements/ directory
- Cross-reference transactions between different document types
- Show your calculations for verification
- Provide a summary of findings at the end
```

### Step 3: Create All 8 Agent Files

Create these files in `.claude/agents/`:

1. `financial-auditor.md`
2. `spending-analyzer.md`
3. `tax-verifier.md`
4. `retirement-analyzer.md`
5. `budget-monitor.md`
6. `cashflow-analyst.md`
7. `document-checker.md`
8. `savings-tracker.md`

### Step 4: Using Agents in Claude Code

```bash
# Invoke an agent from the command line
claude @financial-auditor "Check January 2024 statements"

# Or use in a conversation
@document-checker verify all files are present
@spending-analyzer analyze Q1 2024 spending patterns
```

---

## Setup for ChatGPT

ChatGPT doesn't have persistent agent definitions, so you'll use the prompts directly.

### Step 1: Prepare Your Files

1. Navigate to `statements/` directory
2. Identify which PDFs you need for your analysis
3. Have `agents.txt` open for reference

### Step 2: Start a New Conversation

1. Go to https://chat.openai.com
2. Start a new chat
3. Copy the relevant agent prompt from `agents.txt`

### Step 3: Upload Documents

ChatGPT supports file uploads (PDF, up to 10 files at once recommended):

**Example: Running Financial Auditor**

1. Copy the Financial Auditor prompt from `agents.txt`
2. Paste it into ChatGPT
3. Upload relevant PDFs:
   - January 2024 checking statement
   - January 2024 savings statement
   - January 2024 utility bills (4 files)
4. Ask: "Please analyze these documents"

### Step 4: Iterative Analysis

For large analyses:
- Start with 1-2 months, then expand
- Use follow-up questions to dig deeper
- Save important findings to a separate document

**Example workflow:**
```
Session 1: Upload Jan-Mar statements → Get Q1 analysis
Session 2: Upload Apr-Jun statements → Get Q2 analysis
Session 3: Compare Q1 vs Q2 findings
Session 4: Upload all 12 months → Get full year summary
```

---

## Setup for Google Gemini

Gemini supports file uploads and can analyze multiple PDFs.

### Step 1: Access Gemini

1. Go to https://gemini.google.com
2. Sign in with your Google account

### Step 2: Prepare Agent Prompt

1. Open `agents.txt`
2. Copy the agent prompt you want to use
3. Modify if needed for Gemini's interface

### Step 3: Upload Files

Gemini allows multiple file uploads:

**Example: Running Spending Pattern Analyzer**

1. Click the attachment icon
2. Upload checking statements (all 12 months)
3. Paste the Spending Pattern Analyzer prompt
4. Add: "The uploaded files are checking account statements for Bob and Jane Doe for all of 2024"
5. Submit

### Step 4: Follow-Up Questions

```
"Show me a breakdown of dining expenses by month"
"Which month had the highest grocery spending?"
"Create a chart showing spending trends"
"What percentage of income goes to Jane's gambling?"
```

---

## Setup for Other AI Systems

### General Setup Process

1. **Identify PDF Reading Capability**: Ensure your AI can read PDF files
2. **Prepare System Prompt**: Use the agent definition as a system prompt
3. **Provide Context**: Give the AI context about the project
4. **Upload Files**: Provide access to the `statements/` directory
5. **Execute Analysis**: Ask specific questions aligned with the agent's purpose

### Using Python + AI APIs

If you want to automate agent analysis programmatically:

**Example: Using OpenAI API**

```python
import openai
from pathlib import Path

# Load agent prompt
with open('agents.txt', 'r') as f:
    agents_content = f.read()

# Extract specific agent prompt (Financial Auditor example)
financial_auditor_prompt = """
You are a financial auditor. Review all documents and verify that:
[... rest of prompt ...]
"""

# List PDF files
bank_statements = list(Path('bank_statements').glob('*.pdf'))

# Create analysis request
client = openai.OpenAI()
response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": financial_auditor_prompt},
        {"role": "user", "content": "Analyze January 2024 statements"}
    ]
    # Note: File upload would be handled separately
)

print(response.choices[0].message.content)
```

---

## Running Agent Analysis

### Recommended Workflow

#### Phase 1: Verification (Days 1-2)
1. **Document Completeness Checker** - Verify all 74 files present
2. **Financial Auditor** - Check for mathematical errors

#### Phase 2: Understanding (Days 3-5)
3. **Spending Pattern Analyzer** - Understand spending habits
4. **Cash Flow Analyst** - Identify cash flow patterns
5. **Budget Compliance Monitor** - Assess budget health

#### Phase 3: Specialized Analysis (Days 6-8)
6. **Savings Goal Tracker** - Track savings progress
7. **Retirement Account Analyzer** - Analyze retirement performance
8. **Tax Document Verifier** - Verify 2023 tax return

### Sample Analysis Session

**Scenario: Complete Financial Health Check**

```bash
# Step 1: Verify completeness
@document-checker "List all files and confirm nothing is missing"

# Step 2: Audit accuracy
@financial-auditor "Check January-March 2024 for any errors"

# Step 3: Analyze spending
@spending-analyzer "Provide complete spending breakdown for Q1 2024"

# Step 4: Check cash flow
@cashflow-analyst "Identify any months with low balances"

# Step 5: Budget analysis
@budget-monitor "Compare spending to 50/30/20 rule"

# Step 6: Savings check
@savings-tracker "Calculate total interest earned in 2024"

# Step 7: Retirement review
@retirement-analyzer "Compare 401k vs 403b performance"

# Step 8: Tax verification
@tax-verifier "Verify 2023 Form 1040 is accurate"
```

### Creating Custom Analysis Reports

**Example: Monthly Financial Summary**

Combine multiple agents:
```
1. Use Document Checker to list January files
2. Use Financial Auditor to verify January accuracy
3. Use Spending Analyzer for January spending breakdown
4. Use Cash Flow Analyst for January cash flow
5. Compile findings into "January 2024 Financial Report"
```

---

## Troubleshooting

### Common Issues

#### Issue: "Cannot read PDF files"

**Solution:**
- Ensure PDFs are not corrupted (open them manually first)
- Try re-generating the PDFs using the Python scripts
- Use a different AI system with better PDF support

#### Issue: "Too many files to upload"

**Solution:**
- Analyze in batches (one month at a time)
- Focus on specific document types (e.g., only checking statements)
- Use command-line tools to extract text from PDFs first

#### Issue: "Agent gives generic responses"

**Solution:**
- Be more specific in your questions
- Reference specific months or transactions
- Ask for numerical analysis rather than general observations
- Example: Instead of "analyze spending," say "calculate total grocery spending for Q1 2024"

#### Issue: "Calculations don't match"

**Solution:**
- Double-check the agent is reading the correct PDFs
- Verify PDF text extraction is accurate
- Manually verify a few calculations
- Remember: Due to randomization, some amounts may vary between runs

### Getting Better Results

**Best Practices:**

1. **Be Specific**: "Calculate interest earned in June 2024" vs "check savings"
2. **Provide Context**: "According to the savings statement..."
3. **Request Evidence**: "Show your calculations step-by-step"
4. **Cross-Reference**: Use multiple agents to verify findings
5. **Save Progress**: Document findings as you go

---

## Advanced Usage

### Creating Custom Agents

You can create additional specialized agents:

**Example: Gambling Expense Analyzer**
```markdown
You are a financial counselor specializing in gambling expenses.

Analyze Jane's DraftKings transactions across all 2024 checking statements:
1. Calculate total spent on gambling per month
2. Identify patterns (day of week, time of month)
3. Calculate as percentage of household income
4. Assess financial impact
5. Provide recommendations for management

Focus specifically on transactions labeled "DraftKings".
```

### Batch Processing

For analyzing all 12 months at once:

```bash
# Create a batch analysis script
for month in {01..12}; do
    echo "Analyzing month $month"
    @spending-analyzer "analyze 2024-$month spending"
    sleep 5  # Avoid rate limits
done
```

### Integration with Other Tools

**Export findings to spreadsheet:**
1. Have agent output data in CSV format
2. Import into Excel/Google Sheets
3. Create charts and visualizations

**Example prompt:**
```
"Create a CSV table with columns: Month, Groceries, Gas, Dining, Utilities, Total
Include all 12 months of 2024"
```

---

## Next Steps

After setting up and running your agents:

1. **Document Findings**: Keep a summary of what each agent discovered
2. **Create Reports**: Compile agent outputs into comprehensive reports
3. **Track Over Time**: Re-run agents periodically to track changes
4. **Customize**: Modify agent prompts based on your specific needs
5. **Share**: Use findings for demonstrations, education, or testing

## Support

For questions or issues:
- Review the `agents.txt` file for agent definitions
- Check `CLAUDE.md` for project documentation
- Review `README.md` for project overview
- Check generated PDFs manually to verify data

---

**Happy Analyzing!** 🤖📊💰
