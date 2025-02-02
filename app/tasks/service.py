from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import models, schemas

class TaskService:
    @staticmethod
    def create_task(db: Session, task: schemas.TaskCreate, user_id: int):
        db_task = models.Task(**task.dict(), creator_id=user_id)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def get_user_tasks(db: Session, user_id: int):
        return db.query(models.Task).filter(models.Task.creator_id == user_id).all()

    @staticmethod
    def delete_task(db: Session, task_id: int, user_id: int):
        task = db.query(models.Task).filter(
            models.Task.id == task_id,
            models.Task.creator_id == user_id
        ).first()
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or you don't have permission to delete it"
            )
        
        db.delete(task)
        db.commit()
        return None

    @staticmethod
    def update_task_description(db: Session, task_id: int, new_description: str, user_id: int):
        task = db.query(models.Task).filter(
            models.Task.id == task_id,
            models.Task.creator_id == user_id
        ).first()
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or you don't have permission to update it"
            )
        
        task.description = new_description
        db.commit()
        db.refresh(task)
        return task