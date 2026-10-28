#!/bin/bash
# ============================================================
# Experiment 2: Git Branching Strategies
# ============================================================
# AIM: To study and implement Git branching strategies
#      (GitFlow, Feature Branching, Trunk-based Development)
#
# Run this script step by step or follow the manual commands below
# ============================================================

echo "=========================================="
echo "  Experiment 2: Git Branching Strategies"
echo "=========================================="

# -------------------------------------------------------
# PART 1: GITFLOW WORKFLOW
# -------------------------------------------------------
echo ""
echo "--- PART 1: GitFlow Workflow ---"

# Initialize a new repo for demo
git init gitflow-demo
cd gitflow-demo
git checkout -b main
echo "# GitFlow Demo" > README.md
git add . && git commit -m "Initial commit"

# 1. Create 'develop' branch (base for all features)
git checkout -b develop
echo "Develop branch initialized" > develop.txt
git add . && git commit -m "chore: initialize develop branch"
echo "[1] Created 'develop' branch"

# 2. Create a Feature Branch (OBS-03: View Books)
git checkout -b feature/view-books develop
echo "Feature: View Books implementation" > ViewBooks.java
git add . && git commit -m "feat(OBS-03): implement view books feature"
echo "[2] Created feature branch: feature/view-books"

# 3. Complete feature and merge back to develop
git checkout develop
git merge --no-ff feature/view-books -m "Merge feature/view-books into develop"
git branch -d feature/view-books
echo "[3] Merged feature/view-books into develop and deleted feature branch"

# 4. Create another Feature Branch (OBS-04: Search Books)
git checkout -b feature/search-books develop
echo "Feature: Search Books implementation" > SearchBooks.java
git add . && git commit -m "feat(OBS-04): implement search books feature"
git checkout develop
git merge --no-ff feature/search-books -m "Merge feature/search-books into develop"
git branch -d feature/search-books
echo "[4] Created and merged feature/search-books"

# 5. Create Release Branch
git checkout -b release/1.0 develop
echo "1.0.0" > version.txt
git add . && git commit -m "chore: bump version to 1.0.0"
echo "[5] Created release/1.0 branch"

# 6. Bug fix on release branch
echo "Release bug fix" > bugfix.txt
git add . && git commit -m "fix: fix critical bug on release branch"

# 7. Merge release into main AND develop
git checkout main
git merge --no-ff release/1.0 -m "Merge release/1.0 into main"
git tag -a v1.0.0 -m "Release version 1.0.0"

git checkout develop
git merge --no-ff release/1.0 -m "Merge release/1.0 back into develop"
git branch -d release/1.0
echo "[7] Merged release/1.0 into main (tagged v1.0.0) and back into develop"

# 8. Create Hotfix Branch
git checkout -b hotfix/critical-login-fix main
echo "Fix: Critical login issue" > hotfix.txt
git add . && git commit -m "fix: resolve critical login issue (OBS-02)"
echo "[8] Created hotfix/critical-login-fix branch"

# 9. Merge hotfix into main AND develop
git checkout main
git merge --no-ff hotfix/critical-login-fix -m "Merge hotfix/critical-login-fix into main"
git tag -a v1.0.1 -m "Hotfix release v1.0.1"

git checkout develop
git merge --no-ff hotfix/critical-login-fix -m "Merge hotfix/critical-login-fix into develop"
git branch -d hotfix/critical-login-fix
echo "[9] Merged hotfix and tagged v1.0.1"

cd ..

# -------------------------------------------------------
# PART 2: FEATURE BRANCH WORKFLOW
# -------------------------------------------------------
echo ""
echo "--- PART 2: Feature Branch Workflow ---"

git init feature-branch-demo
cd feature-branch-demo
git checkout -b main
echo "# Feature Branch Demo" > README.md
git add . && git commit -m "Initial commit on main"

# Feature 1
git checkout -b feature/user-registration main
echo "User registration code" > Registration.java
git add . && git commit -m "feat: add user registration (OBS-01)"
git checkout main
git merge --no-ff feature/user-registration -m "Merge feature/user-registration"
git branch -d feature/user-registration
echo "[Feature Branch] Merged feature/user-registration"

# Feature 2 (parallel development simulation)
git checkout -b feature/book-search main
echo "Book search code" > BookSearch.java
git add . && git commit -m "feat: add book search (OBS-04)"
git checkout main
git merge --no-ff feature/book-search -m "Merge feature/book-search"
git branch -d feature/book-search
echo "[Feature Branch] Merged feature/book-search"

cd ..

# -------------------------------------------------------
# PART 3: TRUNK-BASED DEVELOPMENT
# -------------------------------------------------------
echo ""
echo "--- PART 3: Trunk-Based Development ---"

git init trunk-based-demo
cd trunk-based-demo
git checkout -b main
echo "# Trunk-Based Demo" > README.md
git add . && git commit -m "Initial commit"

# All developers commit directly to main (short-lived branches)
git checkout -b short-feature/login main
echo "Short login feature" > Login.java
git add . && git commit -m "feat: implement login"
git checkout main
git merge short-feature/login -m "Merge short-feature/login"
git branch -d short-feature/login
echo "[Trunk-Based] Short-lived feature branch merged quickly to main"

# Feature flags for incomplete features
cat << 'EOF' > feature_flags.txt
# Feature Flags Configuration
# Enable/disable features without creating branches
FEATURE_RECOMMENDATION_ENGINE=false  # In development
FEATURE_PAYMENT_GATEWAY=false        # Pending
FEATURE_USER_REGISTRATION=true       # Complete
FEATURE_VIEW_BOOKS=true              # Complete
EOF
git add . && git commit -m "chore: add feature flags for trunk-based development"

cd ..

# -------------------------------------------------------
# SUMMARY: Show all branch history
# -------------------------------------------------------
echo ""
echo "=========================================="
echo "  Git Branch History Summary"
echo "=========================================="
echo ""
echo "GitFlow Demo:"
cd gitflow-demo && git log --oneline --graph --all | head -20 && cd ..
echo ""
echo "Feature Branch Demo:"
cd feature-branch-demo && git log --oneline --graph --all | head -10 && cd ..
echo ""
echo "Trunk-Based Demo:"
cd trunk-based-demo && git log --oneline --graph --all | head -10 && cd ..
echo ""
echo "Experiment 2 Complete!"
