from app.models.user_model import User
from app.models.todo_model import Todo
from app.schemas.todo_schemas import TodoCreate, TodoUpdate

from typing import List
from uuid import UUID
from datetime import datetime, timezone


class TodoService:
    @staticmethod
    async def list_todos(user: User) -> List[Todo]:
        todos = await Todo.find(Todo.owner.id == user.id).to_list()
        return todos

    @staticmethod
    async def create_todo(data: TodoCreate, user: User):
        todo = Todo(**data.model_dump(), owner=user)
        # The method "dict" in class "BaseModel" is deprecated
        # The dict method is deprecated; use model_dump instead.
        return await todo.insert()
    
    @staticmethod
    async def retrieve_todo(todo_id: UUID, user:User):
        return await Todo.find_one(Todo.todo_id == todo_id, Todo.owner.id == user.id)

    @staticmethod
    async def update_todo(todo_id: UUID, data: TodoUpdate, user: User):
        todo = await TodoService.retrieve_todo(todo_id, user)
        if todo:
            data_dict = data.model_dump(exclude_unset=True)
            data_dict['updated_at'] = datetime.now(timezone.utc)
            await todo.update({"$set": data_dict})
            await todo.save()
            return todo
        else:
            return None
    
    @staticmethod
    async def delete_todo(todo_id: UUID, user:User):
        todo = await TodoService.retrieve_todo(todo_id, user)
        if todo:
            await todo.delete()
        return None

