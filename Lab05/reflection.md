# Reflection - Static Code Analysis

## 1. What is static code analysis?
Static code analysis examines source code without executing it to identify potential bugs, security weaknesses, and code-quality problems.

## 2. Tools used
- Pylint: checks code quality, naming, documentation, and common programming mistakes.
- Bandit: identifies potential security vulnerabilities in Python code.
- Flake8: checks Python style and formatting issues.

## 3. Issues identified and corrected
The original code contained unsafe use of eval(), MD5 hashing, insecure random PIN generation, broad exception handling, shell command execution, unused imports, and style violations. These were addressed by replacing unsafe approaches, improving exception handling, removing unused imports, and correcting formatting.

## 4. Final results
- Pylint: 10.00/10.
- Bandit: no issues identified.
- Flake8: no violations reported.

## 5. Learning outcome
This lab demonstrated how static analysis tools help improve security, readability, maintainability, and consistency. Running the tools before and after making changes also provided measurable evidence of improvement.
