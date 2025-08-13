from typing import Optional

from pydantic import BaseModel, PositiveInt, StrictBool, constr


# Base model with global config
class StrictBaseModel(BaseModel):
    model_config = {"extra": "forbid"}  # No extra fields allowed anywhere


class TaskCreate(StrictBaseModel):
    title: constr(min_length=1, max_length=100)


class TaskOut(StrictBaseModel):
    id: PositiveInt
    title: constr(min_length=1, max_length=100)
    completed: StrictBool


class TaskUpdate(StrictBaseModel):
    title: constr(min_length=1, max_length=100)
    completed: StrictBool


class TaskOptional(StrictBaseModel):
    title: Optional[constr(min_length=1, max_length=100)] = None
    completed: Optional[StrictBool] = None
