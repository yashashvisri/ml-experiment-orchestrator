import pytest
from app.reporting.markdown_generator import generate_markdown_report
from app.reporting.pdf_builder import build_pdf_report

def test_markdown_report_generation():
    dummy_data = {
        "project": {"name": "Test Project", "description": "Benchmark project"},
        "datasets": [{"name": "iris.csv", "size_kb": 12.5}],
        "runs": [{"name": "trial_1", "experiment_name": "baseline", "status": "FINISHED", "metrics": {"accuracy": 0.95}, "params": {"max_depth": 5}}],
        "total_runs": 1,
        "best_run": {"name": "trial_1", "metrics": {"accuracy": 0.95}, "params": {"max_depth": 5}}
    }
    md = generate_markdown_report(dummy_data, ai_narrative="Strong convergence observed.")
    assert "Test Project" in md
    assert "iris.csv" in md
    assert "Strong convergence observed." in md

def test_pdf_report_generation():
    dummy_data = {
        "project": {"name": "Test Project", "description": "Benchmark project"},
        "datasets": [{"name": "iris.csv", "size_kb": 12.5}],
        "runs": [{"name": "trial_1", "experiment_name": "baseline", "status": "FINISHED", "metrics": {"accuracy": 0.95}, "params": {"max_depth": 5}}],
        "total_runs": 1,
        "best_run": {"name": "trial_1", "metrics": {"accuracy": 0.95}, "params": {"max_depth": 5}}
    }
    pdf_bytes = build_pdf_report(dummy_data, ai_narrative="Strong convergence observed.")
    assert len(pdf_bytes) > 500
    assert pdf_bytes.startswith(b"%PDF")
