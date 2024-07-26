from beanie import Document, Indexed, Link, before_event, Insert, Replace, Update
from uuid import UUID, uuid4
from pydantic import Field
from datetime import datetime, timezone

from app.models.user_model import User


class Todo(Document):
    todo_id: UUID = Field(default_factory=uuid4, unique=True)
    status: bool = False
    title: Indexed(str)
    description: str = None
    created_at: datetime = Field(datetime.now(timezone.utc))
    updated_at: datetime = Field(datetime.now(timezone.utc))
    owner: Link[User]

    def __repr__(self) -> str:
        return f"<Todo {self.title}>"

    def __str__(self) -> str:
        return self.title

    def __hash__(self) -> int:
        return hash(self.title)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Todo):
            return self.todo_id == other.todo_id
        return False
    
    @before_event([Replace, Insert, Update])
    def update_updated_at(self):
        self.updated_at = datetime.now(timezone.utc)
        print(f"------{self.updated_at}-------{self.created_at}")

    class Settings:
        name = "todos"  # 指定集合名称   
