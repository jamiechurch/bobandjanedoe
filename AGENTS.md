# Repository Guidelines

## Project Structure & Module Organization
- Core generators live at `generate_statements.py`, `generate_savings_statements.py`, and `generate_retirement_statements.py`; each produces PDFs into `bank_statements/`.
- `requirements.txt` lists runtime dependencies (mainly `fpdf2`); `venv/` is local-only and should not be committed.
- `bank_statements/` already contains sample outputs; regenerate when logic changes to keep examples in sync.

## Build, Test, and Development Commands
- Install deps: `python -m venv venv && source venv/bin/activate && pip install -r requirements.txt`.
- Generate checking statements: `python generate_statements.py`.
- Generate savings statements: `python generate_savings_statements.py`.
- Generate retirement statements: `python generate_retirement_statements.py`.
- Rebuild everything: run all three scripts above; PDFs land in `bank_statements/` and overwrite existing files.

## Coding Style & Naming Conventions
- Python 3.x with 4-space indentation; prefer explicit helper functions over in-line logic.
- Constants and template data stay in UPPER_SNAKE_CASE dictionaries/lists; keep account metadata grouped near the top of each script.
- Use f-strings for formatting currency and dates; keep PDF formatting values (fonts, colors, layout numbers) collected near their usage with short comments when non-obvious.
- Preserve deterministic naming for outputs: `DoE_Statement_YYYY_MM_Month.pdf`, `DoE_Savings_YYYY_MM_Month.pdf`, `Bob_Doe_401k_YYYY_Annual_Statement.pdf`, `Jane_Doe_403b_YYYY_Annual_Statement.pdf`.

## Testing Guidelines
- No automated test suite; validate by running the generators and confirming expected file counts and names in `bank_statements/`.
- Spot-check PDFs for balanced beginning/ending totals and realistic transaction flows; ensure interest and contribution math aligns with configured rates.
- When altering randomization, keep ranges realistic and avoid negative balances unless intentional.

## Commit & Pull Request Guidelines
- Commit messages: concise, present tense, and scoped (e.g., `Refine savings interest calculations`).
- Include a short summary of generated outputs impacted; update or regenerate sample PDFs when logic changes.
- PRs should note what was run (`python generate_*`) and any manual checks on PDFs; link related issues and add before/after notes if layout or amounts changed.

## Security & Data Handling
- All data is fictional; do not introduce real personal data or proprietary numbers.
- Keep tokens/keys out of the codebase; use local environment variables if future integrations are added.
