from fastapi import FastAPI

app = FastAPI(
    title="ML Experiment Orchestrator API",
    description="Backend API for managing ML experiments, datasets, AI agents, and reports.",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Welcome to the ML Experiment Orchestrator API!"
    }