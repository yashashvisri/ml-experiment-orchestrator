# 🏗️ System Architecture & Engineering Design

This document details the software design patterns, architectural choices, and technical trade-offs implemented throughout the **ML Experiment Orchestrator**.

![Architecture Flow](docs/assets/architecture_diagram.svg)

---

## 🏛️ Layered Decoupled Architecture

The backend strictly adheres to Clean Architecture and the Repository Pattern across 5 distinct layers:

```text
[HTTP Requests] ➔ Controller / Endpoint Layer (app/api/v1/)
                        │
                        ▼
                Service Layer (app/services/)
                        │
                        ▼
                Repository Layer (app/repositories/)
                        │
                        ▼
                Database Layer (PostgreSQL + SQLAlchemy ORM)
```

### 1. Controller / Endpoints Layer (`app/api/v1/endpoints/`)
- Pure FastAPI routes handling HTTP request parsing, Pydantic validation, status codes, and HTTP exceptions.
- Dependency injection handles JWT bearer authentication (`get_current_user`) and database session lifecycle (`get_db`).

### 2. Service Layer (`app/services/`)
- Encapsulates business logic, access control authorization (ensuring users only access their own projects), metric aggregation, and background job dispatches.
- Interacts with ML engines (Optuna, Scikit-Learn, LightGBM, XGBoost) and reporting pipelines (ReportLab, Markdown).

### 3. Repository Layer (`app/repositories/`)
- Abstract data-access layer preventing raw database queries from leaking into business services.
- Clean CRUD interfaces for `Project`, `Dataset`, `Experiment`, and `Run` entities.

### 4. Database Layer (`app/database/`, `app/models/`)
- SQLAlchemy 2.0 ORM with PostgreSQL backend.
- Alembic schema migrations enabling transactional data definition changes.
- Connection pooling with scoped sessions.
