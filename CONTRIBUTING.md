# 🤝 Contributing to ML Experiment Orchestrator

Thank you for your interest in contributing to the **ML Experiment Orchestrator**! We welcome bug reports, feature requests, and code contributions.

---

## 🛠️ Local Development Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yashashvisri/ml-experiment-orchestrator.git
   cd ml-experiment-orchestrator
   ```

2. **Backend Setup:**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements/base.txt -r requirements/test.txt
   alembic upgrade head
   uvicorn app.main:app --reload
   ```

3. **Frontend Setup:**
   ```bash
   cd ../frontend
   streamlit run app.py
   ```

4. **Run with Docker:**
   ```bash
   docker-compose up --build
   ```

---

## 🧪 Running Tests
```bash
cd backend
PYTHONPATH=. pytest tests/
```

---

## 🌿 Branching & Commit Guidelines
- Use conventional commit messages: `feat:`, `fix:`, `docs:`, `chore:`, `test:`.
- Create feature branches: `git checkout -b feature/your-feature-name`.
