from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate


def get_tasks(db: Session) -> List[Task]:
    """Get all tasks"""
    return db.query(Task).all()


def get_task(db: Session, task_id: str) -> Optional[Task]:
    """Get a task by ID"""
    return db.query(Task).filter(Task.id == task_id).first()


def create_task(db: Session, task: TaskCreate) -> Task:
    """Create a new task with default status TODO"""
    db_task = Task(
        title=task.title,
        description=task.description,
        status=TaskStatus.TODO  # Default status is TODO (BACKLOG)
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: str, task_update: TaskUpdate) -> Optional[Task]:
    """Update a task's title and/or description"""
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    
    # Update only provided fields
    if task_update.title is not None:
        db_task.title = task_update.title
    if task_update.description is not None:
        db_task.description = task_update.description
    
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: str) -> bool:
    """Delete a task"""
    db_task = get_task(db, task_id)
    if not db_task:
        return False
    
    db.delete(db_task)
    db.commit()
    return True

