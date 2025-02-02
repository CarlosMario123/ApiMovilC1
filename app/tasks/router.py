from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..config.database import get_db
from ..auth.dependencies import get_current_user
from . import schemas, service
from ..users.models import User

router = APIRouter(prefix="/tasks", tags=["tasks"])
task_service = service.TaskService()

@router.post("/", response_model=schemas.TaskResponse)
def create_task(
    task: schemas.TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return task_service.create_task(db, task, current_user.id)

@router.get("/", response_model=List[schemas.TaskResponse])
def read_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return task_service.get_user_tasks(db, current_user.id)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return task_service.delete_task(db, task_id, current_user.id)

@router.patch("/{task_id}", response_model=schemas.TaskResponse)
def update_task_description(
    task_id: int,
    task_update: schemas.TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return task_service.update_task_description(db, task_id, task_update.description, current_user.id)