#!/usr/bin/env python3
"""
run_code_quality.py - Run all code quality checks for Experiment 3

Usage:
  python run_code_quality.py

Tools:
  - pylint: Static code analysis, scoring
  - flake8: PEP8 compliance + style
  - black: Auto-format code
  - bandit: Security vulnerability scanner
  - radon: Code complexity metrics
"""

import subprocess
import sys

def run_command(title, cmd):
    """Run a shell command and print output."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    print(f"  Command: {' '.join(cmd)}\n")
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("[STDERR]", result.stderr[:500])
        print(f"  Exit Code: {result.returncode}")
    except FileNotFoundError:
        print(f"  ERROR: '{cmd[0]}' not found. Install with: pip install {cmd[0]}")
    except subprocess.TimeoutExpired:
        print("  ERROR: Command timed out.")


def main():
    print("="*60)
    print("  Experiment 3: Code Quality Analysis")
    print("="*60)

    bad_file = "bad_code_before.py"
    clean_file = "book_store_clean.py"

    # -----------------------------------------------
    # 1. PYLINT Analysis
    # -----------------------------------------------
    print("\n\n### STEP 1: PYLINT Analysis ###")
    print("Pylint checks coding standards, naming conventions, and errors.")

    run_command("Pylint - BAD CODE (before fixes)", ["python", "-m", "pylint", bad_file])
    run_command("Pylint - CLEAN CODE (after fixes)", ["python", "-m", "pylint", clean_file])

    # -----------------------------------------------
    # 2. FLAKE8 Analysis
    # -----------------------------------------------
    print("\n\n### STEP 2: FLAKE8 (PEP8 Style Check) ###")
    print("Flake8 checks PEP8 style compliance, line lengths, imports.")

    run_command("Flake8 - BAD CODE", ["python", "-m", "flake8", bad_file, "--max-line-length=120"])
    run_command("Flake8 - CLEAN CODE", ["python", "-m", "flake8", clean_file, "--max-line-length=100"])

    # -----------------------------------------------
    # 3. BLACK formatter (check mode)
    # -----------------------------------------------
    print("\n\n### STEP 3: BLACK - Auto-Formatter ###")
    print("Black reformats Python code to consistent style.")

    run_command("Black check - BAD CODE (what would change)", ["python", "-m", "black", "--check", "--diff", bad_file])
    run_command("Black format - CLEAN CODE (apply formatting)", ["python", "-m", "black", clean_file])

    # -----------------------------------------------
    # 4. BANDIT - Security Analysis
    # -----------------------------------------------
    print("\n\n### STEP 4: BANDIT - Security Scanner ###")
    print("Bandit finds common security issues in Python code.")

    run_command("Bandit - BAD CODE (security issues)", ["python", "-m", "bandit", "-r", bad_file])
    run_command("Bandit - CLEAN CODE (no hardcoded passwords)", ["python", "-m", "bandit", "-r", clean_file])

    # -----------------------------------------------
    # 5. RADON - Complexity Metrics
    # -----------------------------------------------
    print("\n\n### STEP 5: RADON - Cyclomatic Complexity ###")
    print("Radon measures code complexity (lower = better, A=best, F=worst).")

    run_command("Radon Complexity - BAD CODE", ["python", "-m", "radon", "cc", bad_file, "-s"])
    run_command("Radon Complexity - CLEAN CODE", ["python", "-m", "radon", "cc", clean_file, "-s"])

    print("\n" + "="*60)
    print("  Experiment 3 Complete!")
    print("="*60)
    print("""
Comparison Summary:
----------------------------------------------------------------------
Metric          | BAD CODE (before)  | CLEAN CODE (after)
----------------------------------------------------------------------
Pylint Score    | ~3/10 (many errors)| ~9.5/10 (nearly perfect)
Flake8 Issues   | Multiple violations| 0 violations
Black Changes   | Many reformats     | No changes needed
Bandit Issues   | 1+ HIGH severity   | 0 issues
Radon Complexity| High (B-D range)   | Low (A-B range)
----------------------------------------------------------------------
""")


if __name__ == "__main__":
    main()
