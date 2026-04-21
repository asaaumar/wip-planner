import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.session import Base, get_db
from app.models.settings import Settings

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_wip.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Setup test database before each test"""
    Base.metadata.create_all(bind=engine)
    
    # Initialize settings with WIP limit = 1
    db = TestingSessionLocal()
    settings = Settings(id=1, wip_limit=1)
    db.add(settings)
    db.commit()
    db.close()
    
    yield
    
    # Cleanup after test
    Base.metadata.drop_all(bind=engine)


def test_can_move_to_in_progress_when_under_limit():
    """Should allow moving to in-progress when under WIP limit"""
    # Create a task
    response = client.post("/tasks/", json={"title": "Test Task"})
    assert response.status_code == 201
    task_id = response.json()["id"]
    
    # Move to in-progress (should succeed, 0 < 1)
    response = client.patch(f"/tasks/{task_id}/status", json={"status": "in-progress"})
    assert response.status_code == 200
    assert response.json()["status"] == "in-progress"


def test_blocks_moving_to_in_progress_when_at_limit():
    """Should block moving to in-progress when at WIP limit"""
    # Create two tasks
    response1 = client.post("/tasks/", json={"title": "Task 1"})
    task1_id = response1.json()["id"]
    
    response2 = client.post("/tasks/", json={"title": "Task 2"})
    task2_id = response2.json()["id"]
    
    # Move first task to in-progress (should succeed)
    response = client.patch(f"/tasks/{task1_id}/status", json={"status": "in-progress"})
    assert response.status_code == 200
    
    # Try to move second task to in-progress (should fail, 1 >= 1)
    response = client.patch(f"/tasks/{task2_id}/status", json={"status": "in-progress"})
    assert response.status_code == 409
    assert "WIP_LIMIT_REACHED" in str(response.json())


def test_allows_moving_to_done_without_wip_check():
    """Should allow moving to done without WIP check"""
    # Create a task and move to in-progress
    response = client.post("/tasks/", json={"title": "Test Task"})
    task_id = response.json()["id"]
    
    client.patch(f"/tasks/{task_id}/status", json={"status": "in-progress"})
    
    # Move to done (should always succeed)
    response = client.patch(f"/tasks/{task_id}/status", json={"status": "done"})
    assert response.status_code == 200
    assert response.json()["status"] == "done"


def test_allows_moving_to_todo_without_wip_check():
    """Should allow moving to todo without WIP check"""
    # Create a task and move to in-progress
    response = client.post("/tasks/", json={"title": "Test Task"})
    task_id = response.json()["id"]
    
    client.patch(f"/tasks/{task_id}/status", json={"status": "in-progress"})
    
    # Move back to todo (should always succeed)
    response = client.patch(f"/tasks/{task_id}/status", json={"status": "todo"})
    assert response.status_code == 200
    assert response.json()["status"] == "todo"
