# 🎓 Agile Software Engineering & DevOps Lab — Practical Exam Master Guide

**Repository:** `https://github.com/Jay-2007-coder/agile.git`  
**Target Tools:** **JIRA** | **MAVEN** | **JENKINS** | **DOCKER** | **GIT**

---

## 📋 Table of Contents
1. [Exam Quick Reference & Cheat Sheet](#-exam-quick-reference--cheat-sheet)
2. [End-to-End Integrated Exam Workflow (The Golden Loop)](#-end-to-end-integrated-exam-workflow-the-golden-loop)
3. [Tool 1: JIRA — Practical Implementation Steps](#1%EF%B8%8F⃣-tool-1-jira--practical-implementation-steps)
4. [Tool 2: MAVEN — Practical Implementation Steps](#2%EF%B8%8F⃣-tool-2-maven--practical-implementation-steps)
5. [Tool 3: JENKINS — Practical Implementation Steps](#3%EF%B8%8F⃣-tool-3-jenkins--practical-implementation-steps)
6. [Tool 4: DOCKER — Practical Implementation Steps](#4%EF%B8%8F⃣-tool-4-docker--practical-implementation-steps)
7. [Lab Experiments 1 to 9 (Execution Steps)](#-lab-experiments-1-to-9-execution-steps)
8. [Top Viva Questions & Answers](#-top-viva-questions--answers)

---

## ⚡ Exam Quick Reference & Cheat Sheet

| Tool | Core Role | Most Common Exam Commands / Actions |
|---|---|---|
| **Jira** | Agile Project Management | Create Project (Scrum) ➔ Backlog ➔ User Stories ➔ Start Sprint ➔ Move to Done |
| **Git** | Version Control | `git checkout -b feature/OBS-01` ➔ `git commit -m "OBS-01: desc"` ➔ `git push origin main` |
| **Maven** | Java Build & Dependency | `mvn clean compile` ➔ `mvn test` ➔ `mvn package` ➔ `java -jar target/*.jar` |
| **Jenkins** | Continuous Integration (CI) | Freestyle Job / Pipeline ➔ Git Poll / Webhook ➔ Invoke Maven ➔ Archive Artifacts |
| **Docker** | Containerization (CD) | `docker build -t app:1.0 .` ➔ `docker run -d -p 5000:5000 --name app-c app:1.0` |

---

## 🔄 End-to-End Integrated Exam Workflow (The Golden Loop)

If the examiner asks you to demonstrate the **complete automated Agile CI/CD cycle**:

```
[1. JIRA]               [2. GIT]                [3. MAVEN]           [4. JENKINS]          [5. DOCKER]
Create Story   ──►  Branch & Code   ──►  Local Test   ──►  Auto-Build CI  ──►  Deploy Container
(OBS-01: Todo)      (commit with ID)      (mvn test)           (Webhook/Poll)        (Port 5000 Live)
       ▲                                                                                   │
       └──────────────────────── Mark OBS-01 as DONE ◄─────────────────────────────────────┘
```

### 5-Minute Exam Demonstration Sequence:
1. **Jira:** Open Jira Board, pick User Story `OBS-01` (User Registration), move from **To Do** ➔ **In Progress**.
2. **Git & Maven:** Open terminal in your project, run `mvn test` to ensure tests pass.
3. **Commit & Push:**
   ```bash
   git add .
   git commit -m "feat(OBS-01): implemented user registration and unit tests"
   git push origin main
   ```
4. **Jenkins:** Open `http://localhost:8080`, view your Jenkins Job/Pipeline triggering automatically. Show the examiner the **Blue Ocean / Console Output** with all stages green.
5. **Docker:** Show the running container:
   ```bash
   docker ps
   curl http://localhost:5000/health
   ```
6. **Jira Completion:** Drag `OBS-01` to **Done** column in Jira.

---

## 1️⃣ TOOL 1: JIRA — Practical Implementation Steps

### Step 1: Create a Scrum Project
1. Log in to Jira (`https://your-domain.atlassian.net` or local Jira).
2. Click **Projects** ➔ **Create Project**.
3. Select **Software Development** ➔ **Scrum**.
4. Choose **Team-managed** or **Company-managed** project.
5. Enter:
   - **Name:** `Online Book Store`
   - **Key:** `OBS` (Every issue will be prefixed: `OBS-1`, `OBS-2`, etc.)
6. Click **Create Project**.

---

### Step 2: Create Epics and User Stories in Product Backlog
1. Navigate to the **Backlog** tab from the left sidebar.
2. Click **+ Create Issue** to add user stories:

| Issue Type | Summary / Title | Description (Agile Format) | Story Points | Priority |
|---|---|---|---|---|
| **Story** | User Registration (`OBS-01`) | **As a** customer, **I want to** register an account with username and password, **so that** I can access bookstore services. | 3 | High |
| **Story** | User Login (`OBS-02`) | **As a** registered customer, **I want to** log in, **so that** I can access my account session securely. | 3 | High |
| **Story** | View All Books (`OBS-03`) | **As a** visitor, **I want to** view all catalog books, **so that** I can browse available titles. | 2 | Medium |
| **Story** | Search Books (`OBS-04`) | **As a** visitor, **I want to** search books by title/author, **so that** I can quickly locate specific books. | 5 | High |
| **Story** | Add New Book (`OBS-05`) | **As an** admin, **I want to** add new books to the inventory, **so that** the catalog stays updated. | 3 | Medium |
| **Bug** | Empty Search Crash (`OBS-06`) | **Bug:** Searching with empty or null keyword causes NullPointerException. Expected: return empty list. | 1 | Highest |

3. Open each issue and assign:
   - **Story Points (Fibonacci):** 1, 2, 3, 5, 8
   - **Assignee:** Yourself
   - **Acceptance Criteria:** Add checkboxes in the description.

---

### Step 3: Plan and Start Sprint 1
1. On the **Backlog** page, click **Create Sprint** (top right of backlog). A section named `OBS Sprint 1` will appear.
2. Drag user stories from **Backlog** into **OBS Sprint 1**:
   - Drag `OBS-01`, `OBS-02`, `OBS-03`, `OBS-04`, `OBS-05`, `OBS-06`.
3. Click **Start Sprint**.
4. In the pop-up modal:
   - **Sprint Name:** `OBS Sprint 1 - Core MVP`
   - **Duration:** `2 weeks` (or custom 1 day for lab demo)
   - **Sprint Goal:** `Deliver user authentication and core book search and management MVP`
5. Click **Start**.

---

### Step 4: Manage the Active Scrum Board
1. Click **Active Sprints / Board** in the left sidebar.
2. You will see 3 columns:
   - **TO DO** (Items selected for sprint)
   - **IN PROGRESS** (Currently being worked on)
   - **DONE** (Implemented, tested, and verified)
3. During the exam demo:
   - Drag `OBS-01` from **TO DO** ➔ **IN PROGRESS**.
   - Make the commit or run test.
   - Drag `OBS-01` from **IN PROGRESS** ➔ **DONE**.

---

### Step 5: Log Bugs & Link Issues
1. Click **+ Create** at the top bar.
2. Select **Issue Type:** `Bug`.
3. Summary: `OBS-06: Fix empty search input handling`.
4. Link it to `OBS-04` (Search Books) using **Linked Issues** ➔ `relates to`.

---

### Step 6: View Agile Reports & Sprint Burndown
1. In Jira sidebar, click **Reports**.
2. Select **Burndown Chart**:
   - Shows remaining story points vs. time.
   - Explain to examiner: *"The guideline shows ideal burndown rate, and the red line shows our actual progress."*
3. Select **Velocity Chart**:
   - Shows commitment vs. completed story points per sprint.

---

## 2️⃣ TOOL 2: MAVEN — Practical Implementation Steps

Maven is an open-source build automation and project management tool primarily for Java projects.

### Step 1: Standard Directory Structure
Ensure your project adheres to the standard Maven directory structure:
```
exp1-agile-cicd/
├── pom.xml
└── src/
    ├── main/
    │   ├── java/com/obs/        # Application code (App.java, Book.java, Services)
    │   └── resources/           # Configuration files (application.properties)
    └── test/
        └── java/com/obs/        # Test code (BookStoreTest.java)
```

---

### Step 2: Key `pom.xml` Anatomy
```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.obs</groupId>
    <artifactId>online-book-store</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>jar</packaging>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <!-- JUnit 5 for Unit Testing -->
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>5.10.0</version>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <!-- Maven Surefire Plugin to execute tests -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.1.2</version>
            </plugin>
            <!-- Maven Shade Plugin for Executable Fat JAR -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-shade-plugin</artifactId>
                <version>3.5.0</version>
                <executions>
                    <execution>
                        <phase>package</phase>
                        <goals><goal>shade</goal></goals>
                        <configuration>
                            <transformers>
                                <transformer implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
                                    <mainClass>com.obs.BookStoreApp</mainClass>
                                </transformer>
                            </transformers>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
```

---

### Step 3: Maven Build Lifecycle Commands (Run from project folder)

```bash
# 1. Clean previous build artifacts (deletes /target folder)
mvn clean

# 2. Compile source code into bytecode (.class files in target/classes)
mvn compile

# 3. Compile test source code and execute unit tests (Surefire plugin)
mvn test

# 4. Run a specific test class only
mvn test -Dtest=BookStoreTest

# 5. Package compiled code and tests into a JAR file in target/
mvn package

# 6. Package skipping tests (emergency exam fix if a test fails)
mvn package -DskipTests

# 7. Install JAR into local ~/.m2 repository for other projects
mvn install

# 8. Check dependency tree (to show examiner dependencies)
mvn dependency:tree
```

---

### Step 4: Run the Maven Packaged JAR
```bash
# Execute the generated JAR file
java -jar target/online-book-store-1.0-SNAPSHOT.jar
```

---

## 3️⃣ TOOL 3: JENKINS — Practical Implementation Steps

Jenkins is an automation server used to automate build, test, and deployment phases (CI/CD).

### Step 1: Start Jenkins Server
Run Jenkins via one of the two standard methods:

**Method A: Native WAR file:**
```bash
java -jar jenkins.war --httpPort=8080
```

**Method B: Docker Container (Recommended & fastest in lab):**
```bash
docker run -d --name jenkins-server -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
```

---

### Step 2: Unlock and Initial Setup
1. Open browser: `http://localhost:8080`.
2. Retrieve the initial Administrator Password:
   - **Windows:** `C:\ProgramData\Jenkins\.jenkins\secrets\initialAdminPassword` (or shown in terminal)
   - **Docker:** `docker exec jenkins-server cat /var/jenkins_home/secrets/initialAdminPassword`
3. Paste password into Jenkins setup screen ➔ Click **Continue**.
4. Select **Install suggested plugins**.
5. Create First Admin User (`admin` / `admin123` or your credentials) ➔ Click **Save and Finish**.

---

### Step 3: Install Required Plugins (If not already installed)
1. Go to **Dashboard** ➔ **Manage Jenkins** ➔ **Plugins**.
2. Click **Available plugins**.
3. Search and check:
   - `Git`
   - `Maven Integration plugin`
   - `Pipeline`
   - `Docker Pipeline`
4. Click **Install without restart**.

---

### Step 4: Configure Tools (JDK, Maven, Git)
1. Go to **Dashboard** ➔ **Manage Jenkins** ➔ **Tools**.
2. **JDK:**
   - Name: `JAVA_HOME`
   - Path: Path to your JDK (e.g., `C:\Program Files\Java\jdk-17` or `/usr/lib/jvm/java-17`)
3. **Git:**
   - Name: `Default`
   - Path to Git: `git` (or path to `git.exe`)
4. **Maven:**
   - Name: `MAVEN_HOME`
   - Click **Install automatically** (or specify local Maven path)
5. Click **Save**.

---

### Step 5: Create a FreeStyle Build Job (Classic Exam Method)
1. From Jenkins Dashboard, click **New Item**.
2. Enter name: `Agile-OBS-Freestyle` ➔ Select **Freestyle project** ➔ Click **OK**.
3. **Source Code Management (SCM):**
   - Select **Git**.
   - Repository URL: `https://github.com/Jay-2007-coder/agile.git`
   - Branch Specifier: `*/main`
4. **Build Triggers:**
   - Check **Poll SCM** ➔ Schedule: `H/5 * * * *` (polls GitHub every 5 minutes).
5. **Build Steps:**
   - Click **Add build step** ➔ Select **Invoke top-level Maven targets**.
   - Maven Version: `MAVEN_HOME`
   - Goals: `clean test package`
   - POM: `implementations/exp1-agile-cicd/pom.xml`
6. **Post-build Actions:**
   - Click **Add post-build action** ➔ **Archive the artifacts**: `**/target/*.jar`
   - Click **Add post-build action** ➔ **Publish JUnit test result report**: `**/target/surefire-reports/*.xml`
7. Click **Save**.
8. Click **Build Now** on the left menu.
9. Click Build `#1` under **Build History** ➔ Click **Console Output** to view the live build log.

---

### Step 6: Create a Declarative Pipeline Job (Modern Exam Method)

1. Dashboard ➔ **New Item** ➔ Name: `Agile-OBS-Pipeline` ➔ Select **Pipeline** ➔ Click **OK**.
2. Scroll to **Pipeline** section at the bottom.
3. Definition: **Pipeline script**.
4. Paste the following complete `Jenkinsfile`:

```groovy
pipeline {
    agent any

    tools {
        maven 'MAVEN_HOME'
        jdk 'JAVA_HOME'
    }

    stages {
        stage('1. Checkout Code') {
            steps {
                echo '=== Pulling Latest Code from Git Repository ==='
                git branch: 'main', url: 'https://github.com/Jay-2007-coder/agile.git'
            }
        }

        stage('2. Maven Compile') {
            steps {
                echo '=== Compiling Java Source Files ==='
                dir('implementations/exp1-agile-cicd') {
                    bat 'mvn clean compile' // Use 'sh' on Linux/Mac, 'bat' on Windows
                }
            }
        }

        stage('3. Maven Run Unit Tests') {
            steps {
                echo '=== Executing JUnit 5 Tests ==='
                dir('implementations/exp1-agile-cicd') {
                    bat 'mvn test'
                }
            }
            post {
                always {
                    junit 'implementations/exp1-agile-cicd/target/surefire-reports/*.xml'
                }
            }
        }

        stage('4. Maven Package (JAR)') {
            steps {
                echo '=== Building Executable JAR Artifact ==='
                dir('implementations/exp1-agile-cicd') {
                    bat 'mvn package -DskipTests'
                }
            }
        }

        stage('5. Docker Build Image') {
            steps {
                echo '=== Building Docker Container Image ==='
                dir('implementations/exp5-docker') {
                    bat 'docker build -t online-book-store:1.0 .'
                }
            }
        }

        stage('6. Docker Deploy & Run') {
            steps {
                echo '=== Running Container on Port 5000 ==='
                bat 'docker stop obs-container || exit 0'
                bat 'docker rm obs-container || exit 0'
                bat 'docker run -d --name obs-container -p 5000:5000 online-book-store:1.0'
            }
        }
    }

    post {
        success {
            echo '🎉 CI/CD Pipeline Completed Successfully! Application Deployed.'
            archiveArtifacts artifacts: 'implementations/exp1-agile-cicd/target/*.jar', fingerprint: true
        }
        failure {
            echo '❌ Pipeline Failed! Please check the console output above.'
        }
    }
}
```
5. Click **Save** ➔ Click **Build Now**.
6. View the visual **Stage View** to show all green boxes to the examiner.

---

## 4️⃣ TOOL 4: DOCKER — Practical Implementation Steps

Docker packages applications and their dependencies into self-contained portable containers.

### Step 1: Anatomy of a Dockerfile
Inside `implementations/exp5-docker/Dockerfile`:
```dockerfile
# Base image with Python runtime
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Copy dependency definition
COPY requirements.txt .

# Install application dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app.py .

# Expose container port to host
EXPOSE 5000

# Healthcheck to monitor container health
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# Command to execute when container starts
CMD ["python", "app.py"]
```

---

### Step 2: Build the Docker Image
```bash
cd implementations/exp5-docker

# Build image with name 'online-book-store' and tag '1.0'
# The dot '.' indicates the current directory contains the Dockerfile
docker build -t online-book-store:1.0 .

# Verify the image is created
docker images
```

---

### Step 3: Run the Docker Container
```bash
# Run container in detached mode (-d), name it 'obs-app', map host port 5000 to container 5000
docker run -d --name obs-app -p 5000:5000 online-book-store:1.0

# Verify container is running
docker ps
```

---

### Step 4: Test the Live Application Inside Docker
```bash
# Test health endpoint
curl http://localhost:5000/health

# Test book catalog endpoint
curl http://localhost:5000/books

# Test searching a book
curl "http://localhost:5000/books/search?q=Python"

# Test user registration endpoint (POST)
curl -X POST http://localhost:5000/users/register \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"jay_student\", \"password\": \"secure123\"}"
```

---

### Step 5: Inspect, Debug, and Logs
```bash
# 1. View logs of running container
docker logs obs-app
docker logs -f obs-app   # Follow logs continuously

# 2. Execute an interactive shell inside the running container
docker exec -it obs-app /bin/sh

# Inside container shell:
# ls -la
# python --version
# exit

# 3. View resource utilization stats (CPU, Memory)
docker stats obs-app --no-stream
```

---

### Step 6: Docker Compose (Multi-Container Execution)
Using `implementations/exp5-docker/docker-compose.yml`:
```yaml
version: '3.8'

services:
  web:
    build: .
    image: online-book-store:latest
    container_name: obs-web
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - PORT=5000
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

**Commands:**
```bash
# Start all services in background
docker compose up -d

# Check running services
docker compose ps

# View aggregate logs
docker compose logs

# Stop and remove containers, networks
docker compose down
```

---

### Step 7: Clean Up Containers & Images
```bash
# Stop the running container
docker stop obs-app

# Remove the stopped container
docker rm obs-app

# Remove the Docker image
docker rmi online-book-store:1.0

# Remove all unused containers, networks, dangling images
docker system prune -f
```

---

## 🔬 Lab Experiments 1 to 9 (Execution Steps)

Here are the direct terminal execution steps for each experiment in the repository:

### 🔹 Experiment 1: Agile Methodology + JIRA + CI/CD (Java)
**Folder:** `implementations/exp1-agile-cicd`
```bash
cd implementations/exp1-agile-cicd
mvn clean test
mvn package
java -jar target/online-book-store-1.0-SNAPSHOT.jar
```

---

### 🔹 Experiment 2: Git Branching Strategies (GitFlow, Feature Branch, Trunk-Based)
**Folder:** `implementations/exp2-git-branching`
```bash
cd implementations/exp2-git-branching

# On Windows PowerShell:
.\run_exp2.ps1

# On Git Bash / Linux:
bash run_exp2.sh
```

---

### 🔹 Experiment 3: Code Quality Analysis (Pylint, Flake8, Bandit, Radon)
**Folder:** `implementations/exp3-code-quality`
```bash
cd implementations/exp3-code-quality
pip install pylint flake8 black bandit radon
python run_code_quality.py
```
- Compare: `bad_code_before.py` (Pylint 3.5/10) vs `book_store_clean.py` (Pylint 9.8/10).

---

### 🔹 Experiment 4: Software Testing (Unit & Integration Testing)
**Folder:** `implementations/exp4-testing`
```bash
cd implementations/exp4-testing
pip install pytest pytest-cov
python -m pytest test_book_store.py -v --cov=book_store_for_testing --cov-report=term-missing
```

---

### 🔹 Experiment 5: Containerization with Docker
**Folder:** `implementations/exp5-docker`
```bash
cd implementations/exp5-docker
docker build -t online-book-store:1.0 .
docker run -d --name obs-app -p 5000:5000 online-book-store:1.0
curl http://localhost:5000/health
docker stop obs-app && docker rm obs-app
```

---

### 🔹 Experiment 6: Monitoring & Logging
**Folder:** `implementations/exp6-monitoring`
```bash
cd implementations/exp6-monitoring
pip install flask prometheus-client psutil
python monitoring_app.py
# Check metrics in second terminal:
curl http://localhost:5001/metrics
curl http://localhost:5001/health
```

---

### 🔹 Experiment 7: MLflow — Experiment Tracking (Iris Classification)
**Folder:** `implementations/exp7-mlflow`
```bash
cd implementations/exp7-mlflow
pip install mlflow scikit-learn pandas numpy matplotlib seaborn
python exp7_mlflow_tracking.py
mlflow ui
# Open browser at http://localhost:5000
```

---

### 🔹 Experiment 8: ML Pipeline with MLflow (House Price Prediction)
**Folder:** `implementations/exp8-ml-pipeline`
```bash
cd implementations/exp8-ml-pipeline
pip install mlflow scikit-learn pandas numpy matplotlib seaborn
python exp8_ml_pipeline.py
mlflow ui
```

---

### 🔹 Experiment 9: Student Performance Prediction (Agile ML Deployment)
**Folder:** `implementations/exp9-student-performance`
```bash
cd implementations/exp9-student-performance
pip install mlflow scikit-learn pandas numpy matplotlib seaborn
python exp9_student_performance.py
mlflow ui
```

---

## 💬 Top Viva Questions & Answers

### 1. What is Agile and how does it differ from Waterfall?
> **Answer:** Agile is an iterative, incremental software development methodology where requirements and solutions evolve through collaborative cross-functional teams. Waterfall is linear and sequential (Requirements ➔ Design ➔ Code ➔ Test ➔ Deploy), where changes late in the lifecycle are very expensive. Agile provides rapid delivery, customer feedback, and flexibility through short Sprints (1-4 weeks).

### 2. What is the difference between Scrum and Kanban in Jira?
> **Answer:** 
> - **Scrum:** Works in timeboxed iterations called Sprints (e.g., 2 weeks). Features fixed sprint goals, sprint backlogs, and velocity tracking.
> - **Kanban:** Focuses on continuous flow without fixed timeboxes. It enforces **Work In Progress (WIP) limits** to avoid bottlenecks.

### 3. What are Maven build phases?
> **Answer:** Maven follows standard build lifecycle phases:
> `validate` ➔ `compile` ➔ `test` ➔ `package` ➔ `verify` ➔ `install` ➔ `deploy`. Executing a later phase automatically runs all preceding phases.

### 4. What is the purpose of `pom.xml`?
> **Answer:** **Project Object Model (`pom.xml`)** is the core configuration file in Maven containing project metadata, dependencies (external libraries), plugins (compiler, surefire for testing, shade/jar packager), build profiles, and Java version configurations.

### 5. What is Continuous Integration (CI) vs Continuous Deployment (CD)?
> **Answer:** 
> - **CI (Continuous Integration):** Automated practice where developers merge code into a shared repository frequently; every push triggers automated compilation, static analysis, and unit testing (e.g., Jenkins or GitHub Actions).
> - **CD (Continuous Delivery/Deployment):** Automatically packaging and deploying the tested build into staging or production environments (e.g., via Docker container deployment).

### 6. What is the difference between a Freestyle job and a Pipeline in Jenkins?
> **Answer:** 
> - **Freestyle Job:** Configured via Jenkins GUI forms; good for simple tasks, but difficult to version control or maintain complex multi-step workflows.
> - **Pipeline:** Defined as code (**Pipeline as Code** via a `Jenkinsfile`), stored alongside source code in Git, supports multi-stage pipelines, parallel execution, and automated rollbacks.

### 7. What is a Docker Image vs a Docker Container?
> **Answer:** 
> - **Docker Image:** An immutable, read-only template with instructions and layers for creating a container (like a class in OOP).
> - **Docker Container:** A runnable, isolated, running instance of an image with a writable container layer (like an instantiated object).

### 8. Explain Docker port mapping `-p 5000:5000`.
> **Answer:** Syntax is `-p <HostPort>:<ContainerPort>`. It binds port `5000` on the physical/host machine to port `5000` inside the isolated container so external clients can communicate with the application over network.

### 9. What is GitFlow and what branches are used?
> **Answer:** GitFlow is a strict branching model:
> - `main`: Production-ready release code.
> - `develop`: Integration branch for features.
> - `feature/*`: New features branched off `develop`.
> - `release/*`: Preparation for new production release.
> - `hotfix/*`: Quick emergency bug fixes branched directly off `main`.

### 10. How do Jira and Git integrate in an Agile workflow?
> **Answer:** By putting the Jira issue key (e.g., `OBS-01`) in Git branch names (`feature/OBS-01-register`) or commit messages (`git commit -m "feat(OBS-01): add user registration"`). Jira automatically links the commit, pull request, and build status directly onto the Jira issue board.

---

**Good luck with your practical exam! 🚀**
