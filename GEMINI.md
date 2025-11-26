# Gemini Context: Fictional Financial Data Generator

This file provides context for the Gemini AI assistant to understand and work with this project.

## Project Overview

This is a Python project designed to generate a comprehensive set of fictional financial documents for a simulated married couple, Bob and Jane Doe. The primary purpose is to create realistic-looking PDF bank statements, savings statements, retirement account statements, and tax forms for the year 2024.

The project is structured around a series of Python scripts, each responsible for generating a specific type of financial document. The output is a collection of PDF files in the `bank_statements/` directory.

**Key Technologies:**
- **Language:** Python 3
- **Primary Library:** `fpdf2` for PDF generation.

**Architecture:**
- The project consists of several standalone Python scripts:
    - `generate_statements.py`: Generates checking account statements.
    - `generate_savings_statements.py`: Generates savings account statements.
    - `generate_retirement_statements.py`: Generates 401(k) and 403(b) retirement statements.
    - `generate_tax_return.py`: (Not yet implemented)
- Each script defines the data and logic for its corresponding document type.
- Configuration data (account numbers, names, income, expenses) is stored as constants at the top of each script.
- The `fpdf2` library is used to construct the PDF documents, with a class-based approach to define headers, footers, and content sections.

## Building and Running

### Prerequisites
- Python 3.8+
- `pip`

### Setup and Installation

1.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Generators

To generate all the financial documents, run the following commands from the project root:

```bash
python generate_statements.py
python generate_savings_statements.py
python generate_retirement_statements.py
```

The generated PDF files will be placed in the `bank_statements/` directory.

## Development Conventions

- **Configuration:** Project-level and script-specific configurations are managed using global constants at the top of each file (e.g., `ACCOUNT_INFO`, `MONTHLY_EXPENSES`).
- **PDF Generation:** The `fpdf2` library is used in an object-oriented manner. A custom class inheriting from `FPDF` is defined in `generate_statements.py` to create a standardized document structure with headers, footers, and consistent styling.
- **Data Simulation:** The transaction data is generated programmatically with a degree of randomness to appear realistic. Functions like `generate_transactions` are responsible for creating the data that is then rendered into the PDF.
- **Modularity:** Each script is self-contained and can be run independently.
- **File Naming:** Generated files follow a consistent naming convention, e.g., `DoE_Statement_2024_01_January.pdf`.
- **No Tests:** There is no formal testing framework set up for this project.
