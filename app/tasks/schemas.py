# schemas.py
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str

class TaskUpdate(BaseModel):
    description: str

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    creator_id: int

    class Config:
        orm_mode = True