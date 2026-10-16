# Lab 5: Static Code Analysis — Restaurant Order System

## 1. Objective

To improve Python code quality, security, and coding style using Pylint, Bandit, and Flake8. The lab involves identifying issues in the assigned program, fixing them, and verifying the improvements through static analysis.

## 2. Project Overview

The Restaurant Order System is a Python program that manages restaurant table orders and kitchen tickets. Its functionality includes placing and voiding orders, checking table status, calculating discounted bills, generating ticket hashes and POS PINs, exporting orders to a text file, and summarizing pending orders.

## 3. Static Analysis Tools

- **Pylint:** Evaluates code quality, naming conventions, documentation, and potential programming errors.
- **Bandit:** Detects potentially insecure coding patterns in Python programs.
- **Flake8:** Checks Python code formatting and compliance with style guidelines.

## 4. Issues Identified and Fixes Applied

The original implementation contained multiple code-quality and security issues.

| Tool | Issue identified | Fix applied |
|---|---|---|
| Pylint | Non-standard function names and missing docstrings | Adopted snake_case naming and added docstrings |
| Pylint | Unused imports and variables | Removed unused code |
| Bandit | Unsafe use of `eval()` | Replaced expression evaluation with validated discount-rate calculations |
| Bandit | Weak MD5 hashing | Replaced MD5 with SHA-256 |
| Bandit | Insecure random number generation for a POS PIN | Used Python's `secrets` module |
| Bandit | Broad exception handling | Replaced it with a safer order-removal operation |
| Bandit | Shell command execution | Replaced shell execution with file handling using `pathlib` |
| Flake8 | Formatting and style violations | Corrected formatting, line lengths, and other style issues |

The detailed issue table is available in `issue_table.md`.

## 5. Before-and-After Analysis Results

The following results were obtained during local testing of the original and cleaned programs.

| Tool | Before | After |
|---|---|---|
| Pylint | 4.81/10 | 10.00/10 |
| Bandit | Security findings reported | No issues identified |
| Flake8 | Style violations reported | No violations reported |

The corresponding reports are included in this directory for comparison.

## 6. Setup and Execution

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the environment on Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

### Install the required tools

```bash
python -m pip install pylint bandit flake8
```

### Run the program

```bash
python restaurant_order_system.py
```

### Run Pylint

```bash
python -m pylint restaurant_order_system.py
```

### Run Bandit

```bash
python -m bandit -r restaurant_order_system.py
```

### Run Flake8

```bash
python -m flake8 restaurant_order_system.py
```

## 7. Repository Contents

- `restaurant_order_system.py` — cleaned Python implementation.
- `restaurant_order_system_before.py` — original implementation for comparison.
- `pylint_report_before.txt` — initial Pylint report.
- `pylint_report_after.txt` — final Pylint report.
- `bandit_report_before.txt` — initial Bandit report.
- `bandit_report_after.txt` — final Bandit report.
- `flake8_report_before.txt` — initial Flake8 report.
- `flake8_report_after.txt` — final Flake8 report.
- `issue_table.md` — issues identified and corresponding fixes.
- `reflection.md` — reflection on static code analysis.
- `README.md` — project overview, setup instructions, and results.

## 8. Conclusion

Static code analysis helped identify and address security weaknesses, code-quality problems, and formatting violations in the Restaurant Order System. The cleaned implementation achieved a Pylint score of 10.00/10, no reported Bandit issues, and no Flake8 violations during local testing.

The before-and-after reports provide evidence of the improvements made to the source code.