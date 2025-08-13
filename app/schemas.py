from typing import Optional

from pydantic import BaseModel, constr, PositiveInt


class TaskCreate(BaseModel):
    title: constr(min_length=1, max_length=100)


class TaskOut(BaseModel):
    id: PositiveInt
    title: constr(min_length=1, max_length=100)
    completed: bool


class TaskUpdate(BaseModel):
    title: constr(min_length=1, max_length=100)
    completed: bool


class TaskOptional(BaseModel):
    title: Optional[constr(min_length=1, max_length=100)] = None
    completed: Optional[bool] = None
