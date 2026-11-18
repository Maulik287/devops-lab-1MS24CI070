import pytest
from fastapi.testclient import TestClient
from app.main import app, todos_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    todos_db.clear()
    yield
    todos_db.clear()

def test_get_todos_empty():
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []

def test_create_todo():
    payload = {"title": "Submit DevOps Lab", "description": "Complete assignment for 25CIAEC59", "completed": False}
    response = client.post("/todos", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Submit DevOps Lab"
    assert data["description"] == "Complete assignment for 25CIAEC59"
    assert data["completed"] is False
    assert len(todos_db) == 1
