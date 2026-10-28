# ============================================================
# Experiment 2: Git Branching Strategies - Windows PowerShell
# ============================================================
# Run each step manually in PowerShell/Git Bash
# ============================================================

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Experiment 2: Git Branching Strategies" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# -------------------------------------------------------
# PART 1: GITFLOW WORKFLOW
# -------------------------------------------------------
# GitFlow has 5 branch types:
#   main     - Production-ready code
#   develop  - Integration branch for features
#   feature/* - New features (branch off develop)
#   release/* - Release preparation (branch off develop)
#   hotfix/*  - Critical production fixes (branch off main)

# STEP 1: Initialize GitFlow project
New-Item -ItemType Directory -Force gitflow-demo
Set-Location gitflow-demo
git init
git checkout -b main
"# Online Book Store - GitFlow Demo" | Out-File README.md
git add .
git commit -m "Initial commit"

# STEP 2: Create develop branch
git checkout -b develop
"Develop initialized" | Out-File develop.txt
git add .
git commit -m "chore: initialize develop branch"

# STEP 3: Feature branch - View Books (OBS-03)
git checkout -b feature/view-books develop
"class ViewBooks { public void display() { } }" | Out-File ViewBooks.java
git add .
git commit -m "feat(OBS-03): implement view books feature"

# STEP 4: Merge feature back to develop
git checkout develop
git merge --no-ff feature/view-books -m "Merge feature/view-books into develop"
git branch -d feature/view-books

# STEP 5: Feature branch - Search Books (OBS-04)
git checkout -b feature/search-books develop
"class SearchBooks { public void search(String q) { } }" | Out-File SearchBooks.java
git add .
git commit -m "feat(OBS-04): implement search books"
git checkout develop
git merge --no-ff feature/search-books -m "Merge feature/search-books into develop"
git branch -d feature/search-books

# STEP 6: Release branch
git checkout -b release/1.0 develop
"1.0.0" | Out-File version.txt
git add .
git commit -m "chore: bump version to 1.0.0 for release"

# STEP 7: Merge release to main and tag
git checkout main
git merge --no-ff release/1.0 -m "Merge release/1.0 into main"
git tag -a v1.0.0 -m "Version 1.0.0"

# STEP 8: Merge release back to develop
git checkout develop
git merge --no-ff release/1.0 -m "Merge release/1.0 back into develop"
git branch -d release/1.0

# STEP 9: Hotfix branch
git checkout -b hotfix/login-fix main
"Fix critical login bug" | Out-File hotfix.txt
git add .
git commit -m "fix(OBS-02): fix critical login issue"
git checkout main
git merge --no-ff hotfix/login-fix -m "Merge hotfix/login-fix into main"
git tag -a v1.0.1 -m "Hotfix v1.0.1"
git checkout develop
git merge --no-ff hotfix/login-fix -m "Merge hotfix/login-fix into develop"
git branch -d hotfix/login-fix

# View the graph
Write-Host "`nGitFlow Branch Graph:" -ForegroundColor Green
git log --oneline --graph --all

Set-Location ..
