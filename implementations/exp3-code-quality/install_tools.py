# ============================================================
# Experiment 3: Code Quality - Pylint, Flake8, SonarQube
# ============================================================
# AIM: To study and use code quality tools for Python code
# TOOLS: Pylint, Flake8, autopep8, black
# ============================================================

# install_dependencies.py - Run this first
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

packages = ["pylint", "flake8", "autopep8", "black", "radon", "bandit"]
for pkg in packages:
    print(f"Installing {pkg}...")
    install(pkg)

print("All code quality tools installed!")
