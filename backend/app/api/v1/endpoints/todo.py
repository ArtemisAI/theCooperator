from fastapi import APIRouter, HTTPException, Body, Depends
from typing import List, Dict
from app.schemas.todo import TodoCreate, TodoUpdate, TodoRead
from app.models.user import User # Assuming User model for dependency
# from app.api.deps import get_current_active_user # Assuming this dependency - Module not found

router = APIRouter()

# In-memory "database"
todos_db: Dict[int, TodoRead] = {}
next_todo_id = 1

@router.post("/", response_model=TodoRead, status_code=201)
async def create_todo(
    todo: TodoCreate,
    # current_user: User = Depends(get_current_active_user) # Optional: if auth is needed
):
    """
    Create a new todo item.
    """
    global next_todo_id
    new_todo = TodoRead(id=next_todo_id, title=todo.title, completed=todo.completed)
    todos_db[next_todo_id] = new_todo
    next_todo_id += 1
    return new_todo

@router.get("/", response_model=List[TodoRead])
async def read_todos(
    skip: int = 0,
    limit: int = 100,
    # current_user: User = Depends(get_current_active_user) # Optional: if auth is needed
):
    """
    Retrieve all todo items.
    """
    return list(todos_db.values())[skip : skip + limit]

@router.get("/{todo_id}", response_model=TodoRead)
async def read_todo(
    todo_id: int,
    # current_user: User = Depends(get_current_active_user) # Optional: if auth is needed
):
    """
    Retrieve a specific todo item by ID.
    """
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos_db[todo_id]

@router.put("/{todo_id}", response_model=TodoRead)
async def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    # current_user: User = Depends(get_current_active_user) # Optional: if auth is needed
):
    """
    Update a specific todo item.
    """
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")

    stored_todo_data = todos_db[todo_id]
    update_data = todo_update.dict(exclude_unset=True)
    updated_todo = stored_todo_data.copy(update=update_data)
    todos_db[todo_id] = updated_todo
    return updated_todo

@router.delete("/{todo_id}", status_code=204)
async def delete_todo(
    todo_id: int,
    # current_user: User = Depends(get_current_active_user) # Optional: if auth is needed
):
    """
    Delete a specific todo item.
    """
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos_db[todo_id]
    return None
