import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "AI Content Strategy Engine API" in response.json()["message"]

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_trending_endpoint():
    response = client.get("/api/v1/trending")
    assert response.status_code == 200
    data = response.json()
    assert "google_trends" in data
    assert "reddit_trends" in data
