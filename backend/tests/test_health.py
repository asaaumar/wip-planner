import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test the health check endpoint returns 200 and correct structure"""
    response = client.get("/health")
    
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "version" in data
    assert data["version"] == "0.1.0"
    assert "service" in data
    assert data["service"] == "wip-planner-backend"


def test_health_endpoint_returns_json():
    """Test the health endpoint returns JSON content type"""
    response = client.get("/health")
    
    assert response.headers["content-type"] == "application/json"


