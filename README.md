# 🚀 AI Experiment Platform (ML Experiment Orchestrator)

> A production-ready AI-powered ML Experiment Management Platform built with **FastAPI, React, PostgreSQL, MLflow, LLMs, RAG, and Agentic AI**.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![React](https://img.shields.io/badge/React-Frontend-blue)
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

# 🎯 Project Goals

- Secure user authentication
- Dataset management
- Experiment orchestration
- Automated model training
- Hyperparameter optimization
- MLflow experiment tracking
- AI-generated experiment summaries
- RAG over experiment history
- Multi-agent AI workflows
- Model versioning
- PDF report generation
- Deployment-ready architecture

---

# 🏗️ Current Progress(Completed)

### Backend Foundation

- FastAPI Setup
- PostgreSQL Integration
- SQLAlchemy ORM
- Alembic Migrations
- Production Project Structure

### Authentication

- User Registration
- Password Hashing (bcrypt)
- JWT Login
- Token Generation
- Token Verification
- Protected Routes
- Current User Endpoint (/me)

### Database

- PostgreSQL Database
- UUID Primary Keys
- User Model
- Alembic Migration System

### Architecture

- Repository Pattern
- Service Layer
- Dependency Injection
- API Versioning
- Pydantic Validation

---

# 🚧 In Progress

- Project Management Module

---

# 📅 Upcoming Features

- Project Dashboard
- Dataset Upload
- Data Validation
- ML Pipeline
- Experiment Tracking
- MLflow Integration
- Hyperparameter Optimization
- Model Comparison
- Artifact Storage
- AI Experiment Assistant
- LangChain Integration
- LangGraph Agents
- RAG Search
- PDF Report Generation
- Docker Support
- CI/CD
- Deployment

---

# 🛠 Tech Stack

## Backend

- Python 3.11
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Pydantic
- Passlib (bcrypt)
- Python-JOSE (JWT)

## Frontend (Upcoming)

- React
- Tailwind CSS
- Axios
- React Router

## Machine Learning (Upcoming)

- Scikit-Learn
- XGBoost
- LightGBM
- CatBoost
- Optuna
- MLflow

## AI Stack (Upcoming)

- OpenAI / Gemini
- LangChain
- LangGraph
- FAISS
- ChromaDB
- Sentence Transformers
- Agentic AI

---

# 📂 Current Project Structure

```text
ml-experiment-orchestrator/
│
├── backend/
│   │
│   ├── alembic/
│   │
│   ├── app/
│   │   │
│   │   ├── api/
│   │   │    └── v1/
│   │   │         ├── endpoints/
│   │   │         └── router.py
│   │   │
│   │   ├── core/
│   │   │
│   │   ├── database/
│   │   │
│   │   ├── dependencies/
│   │   │
│   │   ├── models/
│   │   │
│   │   ├── repositories/
│   │   │
│   │   ├── schemas/
│   │   │
│   │   ├── services/
│   │   │
│   │   └── main.py
│   │
│   ├── requirements/
│   │
│   └── .env
│
└── frontend/ (Coming Soon)
```

---

# 🔐 Authentication Flow

```text
Register
     │
     ▼
Hash Password (bcrypt)
     │
     ▼
Store User
     │
     ▼
Login
     │
     ▼
Verify Password
     │
     ▼
Generate JWT
     │
     ▼
Protected Routes
     │
     ▼
Current User
```

---

# 🧠 Software Architecture

```text
Client
   │
   ▼
API Layer
   │
   ▼
Service Layer
   │
   ▼
Repository Layer
   │
   ▼
Database
```

Each layer has a single responsibility:

- **API Layer** → Handles HTTP requests/responses
- **Service Layer** → Business logic
- **Repository Layer** → Database operations
- **Database Layer** → PostgreSQL persistence

---

# 🔑 Implemented REST APIs

| Method | Endpoint | Status |
|---------|----------|--------|
| POST | `/api/v1/auth/register` | ✅ |
| POST | `/api/v1/auth/login` | ✅ |
| GET | `/api/v1/auth/me` | ✅ |

---

# 🗄 Database

Current Tables

- users
- alembic_version

---

# 📚 Learning Objectives

This project demonstrates:

- Backend Engineering
- Machine Learning Engineering
- AI Engineering
- MLOps
- API Development
- Database Design
- JWT Authentication
- Clean Architecture
- Repository Pattern
- Dependency Injection
- Production Software Design

---

# 📈 Roadmap

- [x] FastAPI Setup
- [x] PostgreSQL Integration
- [x] SQLAlchemy ORM
- [x] Alembic Migrations
- [x] User Authentication
- [x] JWT Authorization
- [ ] Project Management
- [ ] Dataset Upload
- [ ] ML Experiment Engine
- [ ] MLflow Tracking
- [ ] Hyperparameter Optimization
- [ ] AI Agents
- [ ] LangGraph Workflows
- [ ] RAG Search
- [ ] React Dashboard
- [ ] Docker
- [ ] CI/CD
- [ ] Deployment

---

# 🚀 Project Status

**Current Version:** `v0.2.0`

**Completion:** **~30%**

The backend foundation and authentication module are complete.

The next milestone is implementing **Project Management**, which will become the core entity for datasets, experiments, and ML workflows.

---

# 👨‍💻 Author

**Yashashvi Srivastava**

AI/ML Engineer | Backend Developer | MLOps Enthusiast

Building production-ready AI applications using Machine Learning, LLMs, Agentic AI, and MLOps best practices.

---

⭐ If you find this project interesting, consider giving it a star!
