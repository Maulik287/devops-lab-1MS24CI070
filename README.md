# DevOps Lab Assignment - Component 1 & 2
**Course Code:** 25CIAEC59 

**USN / Student ID:** 1MS24CI070  
**Repository:** [https://github.com/Maulik287/devops-lab-1MS24CI070](https://github.com/Maulik287/devops-lab-1MS24CI070)

---

## 📋 Project Overview
This repository contains the complete implementation for **Component 1** (CI/CD Pipeline with Git, Jenkins & GitHub Actions) and **Component 2** (Configuration Management with Ansible & Containerized Orchestration with Kubernetes) for a production-ready **FastAPI Todo REST API**.

The pipeline models a continuous assembly line:  
**Code & Git Version Control** ➔ **Automated Testing & Build (Jenkins & GitHub Actions)** ➔ **Server Configuration Management (Ansible)** ➔ **Container Packaging (Multi-Stage Docker)** ➔ **Orchestration & Scaling (Kubernetes)**.

---

## 🏗️ Architecture & Technology Stack
- **Application Backend:** Python 3.11 / 3.14, FastAPI, Uvicorn, Pydantic
- **Testing Framework:** Pytest (Unit tests covering `/health`, `/todos` list, `/todos` create)
- **Version Control:** Git (Feature branching workflow: `feature/health-endpoint` merged into `main` using `--no-ff`)
- **CI/CD Automation:** Jenkins (Declarative Pipeline with `archiveArtifacts`) & GitHub Actions CI (`.github/workflows/ci.yml`)
- **Configuration Management:** Ansible (`inventory.ini`, `playbook.yml`, galaxy role `webapp` with variables and event-driven handlers)
- **Containerization:** Multi-stage `Dockerfile` (Slim runtime image, health check probe, unprivileged execution)
- **Container Orchestration:** Kubernetes manifests (`ConfigMap`, `Deployment` with 3 replicas and liveness/readiness probes, `Service` NodePort)

---

## 📂 Repository Structure
```
.
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI workflow (CI enhancement)
├── ansible/
│   ├── inventory.ini            # Ansible inventory file
│   ├── playbook.yml             # Main playbook invoking the webapp role
│   └── roles/
│       └── webapp/              # Ansible Galaxy role structure
│           ├── defaults/
│           │   └── main.yml     # Role default variables (app_port: 8000)
│           ├── handlers/
│           │   └── main.yml     # Restart handler triggered only on change
│           └── tasks/
│               └── main.yml     # Artifact deployment and dependency tasks
├── app/
│   ├── __init__.py
│   └── main.py                  # FastAPI REST API (GET /health, GET /todos, POST /todos)
├── k8s/
│   ├── configmap.yaml           # Kubernetes ConfigMap (APP_PORT, APP_ENV)
│   ├── deployment.yaml          # 3 replicas, resource limits, liveness & readiness probes
│   └── service.yaml             # NodePort Service exposing port 8000
├── tests/
│   ├── __init__.py
│   └── test_main.py             # 3 Pytest unit tests
├── Dockerfile                   # Multi-stage production Dockerfile
├── Jenkinsfile                  # Declarative Jenkins pipeline with artifact archiving
├── repo_link.txt                # Repository reference URL
├── requirements.txt             # Python dependencies
└── README.md                    # Complete project documentation
```

---

## 🚀 Component 1: Application, Tests & CI/CD Pipeline

### 1. REST API Specification (`app/main.py`)
- `GET /health`: Health probe endpoint returning service status, name, and version.
- `GET /todos`: Retrieves list of current todos.
- `POST /todos`: Creates and stores a new todo item.
- Environment-driven port configuration via `PORT` or `APP_PORT` (defaults to 8000).

### 2. Pytest Unit Tests (`tests/test_main.py`)
Run the test suite locally:
```bash
pytest -v tests/
```
Output:
- `test_health_check`: Verifies HTTP 200 and healthy JSON payload.
- `test_get_todos_empty`: Verifies empty list retrieval.
- `test_create_todo`: Verifies todo item creation and field persistence.

### 3. Git Branching & Merge History
The repository history demonstrates a strict feature-branch workflow:
1. Initial base commit on branch `main`.
2. Feature branch `feature/health-endpoint` created.
3. Health check endpoint and unit test added and committed.
4. Non-fast-forward merge back to `main` (`git merge --no-ff feature/health-endpoint`) showing branching topology in `git log --graph --oneline --all`.

### 4. Jenkins Declarative Pipeline (`Jenkinsfile`)
Defines four discrete stages:
1. **Checkout:** Clones the repository via SCM.
2. **Install Dependencies:** Creates virtualenv and installs `requirements.txt`.
3. **Run Unit Tests:** Executes pytest with JUnit XML report generation.
4. **Package Artifact:** Creates a compressed tarball (`dist/app-artifact.tar.gz`).
5. **Post-Build Action:** Archives the artifact using `archiveArtifacts`.

### 5. CI Enhancement: GitHub Actions (`.github/workflows/ci.yml`)
Automatically triggers on every push and pull request to test code against Python and upload the built tarball artifact to GitHub Actions artifacts.

---

## ⚙️ Component 2: Ansible Configuration Management & Kubernetes

### 1. Ansible Playbook & Role (`ansible/`)
- Target inventory: `ansible/inventory.ini`
- Custom Role: `ansible/roles/webapp/` generated via `ansible-galaxy init`
- Variable configuration: `app_port: 8000`, `app_name: todo-api`
- Idempotent tasks: Unarchives `dist/app-artifact.tar.gz` and installs dependencies
- Event-driven handler: Notifies `restart webapp service` whenever files change

Execute the playbook:
```bash
ansible-playbook -i ansible/inventory.ini ansible/playbook.yml
```

### 2. Multi-Stage Docker Container (`Dockerfile`)
- **Stage 1 (Builder):** Installs Python packages into user location.
- **Stage 2 (Runner):** Lightweight runtime copying only built wheels and app code, with built-in `HEALTHCHECK` probe.

Build and run locally:
```bash
# Build the Docker image
docker build -t devops-todo-api:v1 .

# Run the container
docker run -d --name todo-api-container -p 8000:8000 devops-todo-api:v1

# Test the health endpoint
curl http://localhost:8000/health
```

### 3. Kubernetes Deployment & Scaling (`k8s/`)
Deploy to any local Kubernetes cluster (Minikube / Kind / Docker Desktop):
```bash
# 1. Apply configuration
kubectl apply -f k8s/configmap.yaml

# 2. Deploy 3 replicas with liveness and readiness probes
kubectl apply -f k8s/deployment.yaml

# 3. Expose via NodePort Service
kubectl apply -f k8s/service.yaml

# 4. Verify deployment and pods
kubectl get pods -l app=todo-api
kubectl get svc todo-api-service

# 5. Demonstrate Horizontal Scaling
kubectl scale deployment todo-api-deployment --replicas=5
kubectl get pods -l app=todo-api

# 6. Scale back down
kubectl scale deployment todo-api-deployment --replicas=3
```

---

## 🧪 Local Verification Checklist
- [x] Pytest suite passes 3/3 unit tests
- [x] Git merge topology reflects `feature/health-endpoint` merged via `--no-ff`
- [x] Jenkinsfile syntax and declarative structure verified
- [x] GitHub Actions workflow configured and valid
- [x] Ansible Galaxy role, variables, and handler configured
- [x] Multi-stage Docker image built and tested
- [x] Container responds to `curl http://localhost:8000/health` with `{"status":"healthy",...}`
