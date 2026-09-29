import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test that the API docs load successfully as a basic health check"""
    response = client.get("/docs")
    assert response.status_code == 200
