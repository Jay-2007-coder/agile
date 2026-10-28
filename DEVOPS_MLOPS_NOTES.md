# 📚 DevOps & MLOps Practical Reference Guide (Experiments 1 – 10)

**Source / Shared Chat Link:** [https://chatgpt.com/share/6ae159bb-1fa8-83e8-937a-c4a9a7630c71](https://chatgpt.com/share/6ae159bb-1fa8-83e8-937a-c4a9a7630c71)  
**Reference File:** [`jay.txt`](file:///c:/Users/jsk89/OneDrive/Desktop/agile/jay.txt)

---

## 📑 Syllabus Overview of Experiments

| Exp # | Experiment Title | Primary Tools |
|---|---|---|
| **Exp 1** | Jira Software Project (Scrum, Epics, Stories, Sprint Board) | Jira |
| **Exp 2** | Git Repository Integration with Jira (Issue Keys in Commits) | Git, Jira |
| **Exp 3** | Dockerize a Sample Web Application | Docker, Python / Flask |
| **Exp 4** | Automated Testing & Quality Checks | Pytest / JUnit |
| **Exp 5** | CI/CD Pipeline Automation | Jenkins / GitHub Actions |
| **Exp 6** | Application Monitoring & System Metrics | Prometheus, Flask |
| **Exp 7** | Student Placement Prediction using MLflow Tracking | Python, Scikit-learn, MLflow |
| **Exp 8** | Loan Approval Classification with MLflow Comparison | Python, Scikit-learn, MLflow |
| **Exp 9** | Employee Attrition Prediction & MLflow Model Registry | Python, Scikit-learn, MLflow |
| **Exp 10** | Apache Airflow: Create & Execute a Simple DAG | Apache Airflow, Docker Compose |

---

## 📌 Experiment 1: Jira Software Project Setup & Sprint Management
### Aim:
Create a Jira Software Project using the Scrum template. Create an Epic and add User Stories, Tasks, and Bugs to the Product Backlog. Create and start a Sprint, define the Sprint Goal, and demonstrate issue tracking using the Scrum Board.

### Step-by-Step Implementation:
1. **Create Project:**
   - Log in to Jira. Select **Projects** ➔ **Create Project** ➔ **Scrum**.
   - Project Name: `Online Book Store` | Key: `OBS`.
2. **Create Backlog Items:**
   - Click **+ Create** in Jira header.
   - **Epic:** `Core User Management`
   - **User Story 1:** `As a user, I want to register an account so that I can log in.` (Key: `OBS-1`)
   - **User Story 2:** `As a user, I want to search for books by title.` (Key: `OBS-2`)
   - **Task:** `Setup MySQL / SQLite database schema.` (Key: `OBS-3`)
   - **Bug:** `Search button crashes on empty input.` (Key: `OBS-4`)
3. **Plan and Start Sprint:**
   - Go to **Backlog** tab. Click **Create Sprint**.
   - Drag `OBS-1`, `OBS-2`, and `OBS-3` into the new Sprint.
   - Click **Start Sprint**.
   - Set Duration: `2 weeks` | Sprint Goal: `Deliver user registration and search MVP`.
4. **Scrum Board Progression:**
   - Move `OBS-1` from **TO DO** ➔ **IN PROGRESS** ➔ **DONE** during development.

---

## 📌 Experiment 2: Git Repository & Jira Integration
### Aim:
Create a Git repository and demonstrate issue tracking by referencing Jira issue keys in commit messages.

### Step-by-Step Implementation:
1. Initialize repository and connect remote:
   ```bash
   git init
   git remote add origin https://github.com/Jay-2007-coder/agile.git
   ```
2. Create feature branch:
   ```bash
   git checkout -b feature/OBS-1-registration
   ```
3. Commit referencing Jira Key `OBS-1`:
   ```bash
   git add .
   git commit -m "OBS-1: implement user registration and password hashing"
   git push origin feature/OBS-1-registration
   ```
4. Merge into main:
   ```bash
   git checkout main
   git merge feature/OBS-1-registration
   git push origin main
   ```
5. In Jira, verify the commit appears linked under issue `OBS-1`.

---

## 📌 Experiment 3: Dockerize a Sample Web Application
### Aim:
Create a Dockerfile, build a Docker image, run a container, and test the web application in a browser.

### Step-by-Step Implementation:
1. **Write Dockerfile:**
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY app.py .
   EXPOSE 5000
   CMD ["python", "app.py"]
   ```
2. **Build Docker Image:**
   ```bash
   docker build -t online-book-store:1.0 .
   docker images
   ```
3. **Run Container:**
   ```bash
   docker run -d --name obs-web -p 5000:5000 online-book-store:1.0
   docker ps
   ```
4. **Test in Browser / Terminal:**
   ```bash
   curl http://localhost:5000/health
   curl http://localhost:5000/books
   ```
5. **Stop & Cleanup:**
   ```bash
   docker stop obs-web && docker rm obs-web
   ```

---

## 📌 Experiment 7: Student Placement Prediction Using MLflow
### Aim:
Develop a Decision Tree / Random Forest classification model to predict whether a student will be Placed or Not Placed based on CGPA, Aptitude, and Technical Skills. Track parameters, metrics, and models using MLflow.

### Step-by-Step Implementation:
1. Install dependencies:
   ```bash
   pip install mlflow scikit-learn pandas numpy
   ```
2. Run training script with MLflow tracking:
   ```bash
   python exp7_mlflow_tracking.py
   ```
3. Launch MLflow UI:
   ```bash
   mlflow ui
   ```
   Open `http://localhost:5000` to inspect runs, parameters (`max_depth`), metrics (`accuracy`, `f1_score`), and the confusion matrix artifact.

---

## 📌 Experiment 8: Loan Approval Prediction with MLflow
### Aim:
Develop a classification model to predict loan approval status. Log different experiments with varying hyperparameters to compare performance in MLflow.

### Step-by-Step Implementation:
1. Prepare dataset features: `ApplicantIncome`, `CoapplicantIncome`, `LoanAmount`, `Credit_History`.
2. Train multiple models:
   - Run 1: Logistic Regression
   - Run 2: Decision Tree (`max_depth=5`)
   - Run 3: Random Forest (`n_estimators=100`)
3. Log parameters & metrics for each run using `mlflow.log_param()` and `mlflow.log_metric()`.
4. Compare models side-by-side in MLflow UI.

---

## 📌 Experiment 9: Employee Attrition Prediction with MLflow
### Aim:
Develop an employee attrition prediction model and register the best performing model in the MLflow Model Registry.

### Step-by-Step Implementation:
1. Preprocess HR attrition data (One-Hot encode categorical features, Standardize numerical features).
2. Train ensemble classifiers (Random Forest, Gradient Boosting).
3. Log metrics (ROC-AUC, Precision, Recall).
4. Register the best model to MLflow Model Registry under name `EmployeeAttritionClassifier`.

---

## 📌 Experiment 10: Create and Execute a DAG in Apache Airflow
### Aim:
Create a Directed Acyclic Graph (DAG) named `simple_dag` with two Python tasks, `task_1` and `task_2`, configure it to run daily, execute it using the Airflow web interface, and monitor task statuses and logs.

### Key Concepts:
- **DAG (Directed Acyclic Graph):** Collection of tasks with directional dependencies and no cycles.
- **Operator:** Defines a single task (e.g., `PythonOperator`, `BashOperator`).
- **Scheduler:** Triggers task instances when dependencies are met.
- **Webserver:** UI at `http://localhost:8080` to trigger, monitor, and inspect logs.

### Airflow DAG Code (`simple_dag.py`):
```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'jay',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def task_1_func():
    print("Executing Task 1: Data Ingestion & Preprocessing completed.")

def task_2_func():
    print("Executing Task 2: Model Training & Evaluation completed.")

with DAG(
    dag_id='simple_dag',
    default_args=default_args,
    description='A simple 2-task DAG for practical demonstration',
    schedule_interval='@daily',
    catchup=False,
) as dag:

    t1 = PythonOperator(
        task_id='task_1',
        python_callable=task_1_func,
    )

    t2 = PythonOperator(
        task_id='task_2',
        python_callable=task_2_func,
    )

    # Dependency: task_1 must complete before task_2 runs
    t1 >> t2
```

### Steps to Run Airflow via Docker Compose:
1. Fetch official `docker-compose.yaml` for Airflow:
   ```bash
   curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.7.0/docker-compose.yaml'
   ```
2. Initialize environment:
   ```bash
   mkdir -p ./dags ./logs ./plugins
   docker compose up airflow-init
   ```
3. Place `simple_dag.py` into `./dags/`.
4. Start Airflow services:
   ```bash
   docker compose up -d
   ```
5. Open browser at `http://localhost:8080` (Default credentials: `airflow` / `airflow`).
6. Unpause `simple_dag` toggle switch, click **Trigger DAG** (Play button), and inspect the **Graph View** and task logs.
