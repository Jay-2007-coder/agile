# 🚀 Agile SE Lab - Complete Experiment Implementations

## Overview

This folder contains complete, ready-to-run implementations for all 9 Agile Software Engineering Lab experiments.

---

## 📁 Folder Structure

```
implementations/
├── exp1-agile-cicd/          # Experiment 1: Agile + JIRA + CI/CD (Java)
├── exp2-git-branching/       # Experiment 2: Git Branching Strategies
├── exp3-code-quality/        # Experiment 3: Code Quality (Pylint/Flake8)
├── exp4-testing/             # Experiment 4: Unit & Integration Testing
├── exp5-docker/              # Experiment 5: Docker Containerization
├── exp6-monitoring/          # Experiment 6: Monitoring & Logging
├── exp7-mlflow/              # Experiment 7: MLflow Experiment Tracking
├── exp8-ml-pipeline/         # Experiment 8: ML Pipeline with MLflow
└── exp9-student-performance/ # Experiment 9: Student Performance Prediction
```

---

## Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Java JDK | 17+ | winget install Microsoft.OpenJDK.17 |
| Maven | 3.9+ | winget install Apache.Maven |
| Python | 3.10+ | winget install Python.Python.3.11 |
| Git | Any | winget install Git.Git |
| Docker Desktop | Latest | https://docker.com/products/docker-desktop |

---

## Experiment 1: Agile + JIRA + CI/CD Pipeline

**Aim:** Implement an Online Book Store using Agile methodology with GitHub Actions CI/CD.

**User Stories (Sprint 1):**
| Story | Feature |
|-------|---------|
| OBS-01 | User Registration |
| OBS-02 | User Login |
| OBS-03 | View All Books |
| OBS-04 | Search Books |
| OBS-05 | Add Book to Database |
| OBS-06 | Bug Fix: Empty Search Handling |

**How to Run:**
```bash
cd exp1-agile-cicd
mvn clean package
mvn test
java -jar target/online-book-store-1.0-SNAPSHOT.jar
```

**CI/CD:** Push to GitHub - GitHub Actions automatically builds and tests.
The workflow file is at `.github/workflows/ci.yml`.

---

## Experiment 2: Git Branching Strategies

**How to Run (Git Bash):**
```bash
cd exp2-git-branching
chmod +x run_exp2.sh
./run_exp2.sh
```

**How to Run (PowerShell):**
```powershell
cd exp2-git-branching
.\run_exp2.ps1
```

---

## Experiment 3: Code Quality

```bash
cd exp3-code-quality
pip install pylint flake8 black bandit radon
python run_code_quality.py
```

---

## Experiment 4: Software Testing

```bash
cd exp4-testing
pip install pytest pytest-cov
python -m pytest test_book_store.py -v --cov=book_store_for_testing
```

---

## Experiment 5: Docker Containerization

```bash
cd exp5-docker
docker build -t online-book-store:1.0 .
docker run -d --name obs-container -p 5000:5000 online-book-store:latest
curl http://localhost:5000/health
curl http://localhost:5000/books
```

---

## Experiment 6: Monitoring and Logging

```bash
cd exp6-monitoring
pip install flask prometheus-client psutil
python monitoring_app.py
curl http://localhost:5001/health
curl http://localhost:5001/metrics
```

---

## Experiment 7: MLflow - Iris Classification

```bash
cd exp7-mlflow
pip install mlflow scikit-learn pandas numpy matplotlib seaborn
python exp7_mlflow_tracking.py
mlflow ui
```
Open http://localhost:5000 to see all runs.

---

## Experiment 8: ML Pipeline - House Price Prediction

```bash
cd exp8-ml-pipeline
pip install mlflow scikit-learn pandas numpy matplotlib seaborn
python exp8_ml_pipeline.py
mlflow ui
```

---

## Experiment 9: Student Performance Prediction

```bash
cd exp9-student-performance
pip install mlflow scikit-learn pandas numpy matplotlib seaborn
python exp9_student_performance.py
mlflow ui
```
Open http://localhost:5000 to see all runs.

---

## Common Issues

| Issue | Solution |
|-------|---------|
| mvn not found | Add Maven to PATH |
| ModuleNotFoundError | pip install -r requirements.txt |
| Docker not starting | Ensure Docker Desktop is running |
| MLflow port 5000 busy | Run: mlflow ui --port 5001 |
| Git not configured | git config --global user.email "you@example.com" |
