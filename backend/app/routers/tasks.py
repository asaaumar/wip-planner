from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.crud import task as task_crud

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


@router.get("/", response_model=List[TaskResponse])
def list_tasks(db: Session = Depends(get_db)):
    """
    Get all tasks
    
    Returns a list of all tasks in the system.
    """
    tasks = task_crud.get_tasks(db)
    return tasks


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """
    Create a new task
    
    Creates a new task with default status 'todo' (BACKLOG).
    
    - **title**: Required, 1-200 characters
    - **description**: Optional, max 2000 characters
    """
    db_task = task_crud.create_task(db, task)
    return db_task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: str, task_update: TaskUpdate, db: Session = Depends(get_db)):
    """
    Update a task's title and/or description
    
    - **title**: Optional, 1-200 characters
    - **description**: Optional, max 2000 characters
    """
    db_task = task_crud.update_task(db, task_id, task_update)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return db_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db: Session = Depends(get_db)):
    """
    Delete a task
    
    Permanently removes a task from the system.
    """
    success = task_crud.delete_task(db, task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return None

