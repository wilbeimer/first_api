from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    title: str

class TaskOut(BaseModel):
    id: int
    title: str
    completed: bool

class TaskUpdate(BaseModel):
    title: str
    completed: bool

class TaskOptional(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None