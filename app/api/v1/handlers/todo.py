from fastapi import APIRouter, Depends
from uuid import UUID
from typing import List

from app.schemas.todo_schemas import TodoOut, TodoCreate, TodoUpdate
from app.models.user_model import User
from app.models.todo_model import Todo
from app.api.depends.user_depends import get_current_user
from app.services.todo_service import TodoService


todo_router = APIRouter()

@todo_router.get('/test')
async def test():
    return {'message': 'todo router working'}

@todo_router.get('/', summary='Get all todos of the user', response_model=List[TodoOut])
async def list(current_user: User = Depends(get_current_user)):
    return await TodoService.list_todos(current_user)


@todo_router.post('/create', summary='Create Todo', response_model=Todo)
async def create_todo(data: TodoCreate, current_user: User = Depends(get_current_user)):
    return await TodoService.create_todo(data, current_user)

@todo_router.get('/{todo_id}', summary='Get a todo by todo_id', response_model=TodoOut)
async def retrieve(todo_id: UUID, current_user: User = Depends(get_current_user)):
    return await TodoService.retrieve_todo(todo_id, current_user)

@todo_router.put('/{todo_id}', summary='update todo by todo_id', response_model=TodoOut)
async def update(todo_id: UUID, data: TodoUpdate, user: User = Depends(get_current_user)):
    return await TodoService.update_todo(todo_id, data, user)

@todo_router.delete('/{todo_id}', summary='delete todo by todo_id')
async def delete(todo_id: UUID, user: User = Depends(get_current_user)):
    await TodoService.delete_todo(todo_id, user)
    return None
