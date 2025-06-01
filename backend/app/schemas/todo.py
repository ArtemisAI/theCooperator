from typing import Optional
from .base import BaseSchema # Import BaseSchema

class TodoBase(BaseSchema): # Inherit from BaseSchema
    title: str
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseSchema): # Inherit from BaseSchema
    title: Optional[str] = None
    completed: Optional[bool] = None

class TodoRead(TodoBase):
    id: int

    # Config class is no longer needed, from_attributes=True is inherited from BaseSchema
