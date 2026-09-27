# Docker Architecture

Our ML Experiment Orchestrator is fully containerized using Docker Compose.

## Services

1. **db**: PostgreSQL 15 database persisting data to a Docker volume.
2. **backend**: FastAPI server (Python 3.11) containing the ML pipeline, LangGraph agents, and API.
3. **frontend**: Streamlit dashboard (Python 3.11).

## Networking
All services communicate over the custom bridge network created by Docker Compose. The frontend reaches the backend at `http://backend:8000`. The backend reaches the database at `postgresql://postgres:password@db:5432/ml_orchestrator`.
