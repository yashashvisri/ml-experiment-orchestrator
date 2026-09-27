# 🚀 AI Experiment Platform (ML Experiment Orchestrator)

> A production-ready AI-powered ML Experiment Management Platform built with **FastAPI, Streamlit, PostgreSQL, MLflow, LLMs, RAG, and Agentic AI**.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)
![Alembic](https://img.shields.io/badge/Alembic-Migrations-orange)
![JWT](https://img.shields.io/badge/JWT-Authentication-success)
![License](https://img.shields.io/badge/License-MIT-green)

---

# 📖 Overview

AI Experiment Platform is a full-stack Machine Learning Experiment Orchestration system that enables users to manage datasets, automate ML experiments, track results, compare models, and leverage AI agents to assist throughout the ML lifecycle.

This project follows **production-grade software engineering practices**, including:

- Layered Architecture
- Repository Pattern
- Service Layer
- JWT Authentication
- Alembic Database Migrations
- Clean Code Principles
- Modular Project Structure

The long-term goal is to build an AI platform comparable to a combination of:

- MLflow
- Weights & Biases
- AutoML Platforms
- LangGraph Agent Systems
- AI Research Assistants

---

# 🏗️ Current Progress (Completed)

### Backend Foundation
- FastAPI Setup
- PostgreSQL Integration
- SQLAlchemy ORM
- Alembic Migrations
- Production Project Structure

### Authentication & Core Entities
- User Registration & JWT Login
- Project Management
- Dataset Upload & Storage

### MLOps & Machine Learning
- **ML Experiment Engine:** Core database structures for Experiments and Runs.
- **MLflow Tracking:** Local tracking server integration (SQLite `mlruns.db`).
- **AutoML Pipeline:** Asynchronous background tasks for non-blocking model training.
- **Hyperparameter Optimization:** Optuna objective functions dynamically tuning `RandomForest`, `XGBoost`, and `LightGBM`.

### Frontend Dashboard
- Pure Python **Streamlit** multi-page application.
- Authentication & JWT Session State handling.
- UIs for managing Projects, uploading Datasets, creating Experiments, and firing off AutoML runs.

---

# 🚧 In Progress

- **AI Agents & LangGraph Workflows:** Orchestrating intelligent agents to analyze datasets, explain MLflow metrics, and assist researchers.

---
# 📅 Upcoming Features

- Model Comparison & Registry
- Artifact Storage (S3 / Local mapping)
- AI Experiment Assistant
- LangChain Integration
- LangGraph Agents
- RAG Search (Vector DB integration)
- PDF Report Generation
- **Docker Support & Containerization (Implemented)**
- CI/CD Pipelines
- Cloud Deployment

---

# 🛠 Tech Stack

## Backend
- Python 3.11
- FastAPI
- SQLAlchemy & Alembic
- PostgreSQL
- Pydantic
- Passlib (bcrypt) & Python-JOSE (JWT)

## Frontend
- Streamlit
- Pandas
- Requests

## Machine Learning & MLOps
- Scikit-Learn
- XGBoost
- LightGBM
- Optuna (Hyperparameter Tuning)
- MLflow (Experiment Tracking)

## AI Stack (Upcoming)
- OpenAI / Gemini
- LangChain & LangGraph
- FAISS / ChromaDB
- Sentence Transformers
- Agentic AI

---

# 📂 Current Project Structure

```text
ml-experiment-orchestrator/
│
├── backend/
│   ├── alembic/
│   ├── app/
│   │   ├── api/          # FastAPI Routes (v1)
│   │   ├── core/         # Config & Security
│   │   ├── database/     # DB Sessions & Base
│   │   ├── dependencies/ # Auth & DI
│   │   ├── ml/           # AutoML Pipeline, Optuna Tuner, Data Loader
│   │   ├── models/       # SQLAlchemy Models
│   │   ├── repositories/ # Data Access Layer
│   │   ├── schemas/      # Pydantic Validation
│   │   ├── services/     # Business Logic
│   │   └── main.py       # Entrypoint
│   ├── requirements/
│   └── .env
│
└── frontend/
    ├── app.py            # Streamlit Entrypoint & Auth UI
    ├── pages/            # Projects, Datasets, Experiments, Runs
    └── utils/            # API wrappers and Session management
```

---

# 🔐 Authentication Flow

```text
Register ➔ Hash Password (bcrypt) ➔ Store User
Login ➔ Verify Password ➔ Generate JWT ➔ Protected Routes ➔ Current User
```

---

# 🧠 Software Architecture

```text
Client ➔ API Layer ➔ Service Layer ➔ Repository Layer ➔ Database
```

Each layer has a single responsibility:
- **API Layer** → Handles HTTP requests/responses, triggers background tasks
- **Service Layer** → Business logic & ML Orchestration
- **Repository Layer** → Database operations
- **Database Layer** → PostgreSQL persistence

---

# 🔑 Implemented REST APIs

| Method | Endpoint | Status |
|---------|----------|--------|
| POST | `/api/v1/auth/register` | ✅ |
| POST | `/api/v1/auth/login` | ✅ |
| GET | `/api/v1/auth/me` | ✅ |
| CRUD | `/api/v1/projects/*` | ✅ |
| CRUD | `/api/v1/projects/{id}/datasets/*` | ✅ |
| CRUD | `/api/v1/projects/{id}/experiments/*` | ✅ |
| POST | `/api/v1/experiments/{id}/runs` | ✅ |
| POST | `/api/v1/experiments/{id}/train` | ✅ (AutoML) |

---

# 📚 Learning Objectives

This project demonstrates:
- Backend Engineering & API Development
- Machine Learning Engineering & MLOps
- AI Engineering & Agentic Workflows
- Database Design & ORMs
- Clean Architecture & Repository Pattern
- Production Software Design

---

# 📈 Roadmap

- [x] FastAPI Setup
- [x] PostgreSQL Integration
- [x] SQLAlchemy ORM
- [x] Alembic Migrations
- [x] User Authentication
- [x] JWT Authorization
- [x] Project Management
- [x] Dataset Upload
- [x] Streamlit Dashboard
- [x] ML Experiment Engine
- [x] MLflow Tracking
- [x] Hyperparameter Optimization
- [x] AI Agents
- [x] LangGraph Workflows
- [x] RAG Search
- [ ] Docker
- [ ] CI/CD
- [ ] Deployment

---

# 🚀 Project Status

**Current Version:** `v0.5.0`

**Completion:** **~75%**

The Backend Foundation, Authentication, Project Management, Dataset Uploads, **Machine Learning Engine**, **Hyperparameter Optimization**, **MLflow tracking**, and **Streamlit Dashboard** are fully integrated and complete. 

The next milestone is integrating the **AI Agents & LangGraph Workflows**, which will introduce intelligent LLM-driven research assistants to interpret ML metrics and guide dataset analysis.

---

# 👨‍💻 Author

**Yashashvi Srivastava**

AI/ML Engineer | Backend Developer | Agentic AI Enthusiast

Building production-ready AI applications using Machine Learning, LLMs, Agentic AI, and MLOps best practices.

---

⭐ If you find this project interesting, consider giving it a star!
