# Static Code Analysis - Issue Table

| Tool | Original issue | Fix applied | Final result |
|---|---|---|---|
| Pylint | Poor naming, missing docstrings, unused imports and variables, and style issues | Improved naming, added docstrings, removed unused imports and variables, and corrected formatting | 10.00/10 |
| Bandit | Use of `eval()`, MD5 hashing, insecure random PIN generation, broad exception handling, and `os.system()` | Removed `eval()`, replaced MD5 with SHA-256, used `secrets` for PIN generation, removed broad exception handling, and replaced shell execution with `pathlib` file handling | No issues identified |
| Flake8 | Unused imports, formatting issues, long lines, and other style violations | Removed unused imports and corrected formatting and code style | No violations reported |
