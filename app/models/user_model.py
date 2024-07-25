from beanie import Document, Indexed
from pydantic import Field, EmailStr
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, Annotated


class User(Document):
    user_id: UUID = Field(default_factory=uuid4)
    username: Indexed(str, unique=True)
    email: Indexed(EmailStr, unique=True)
    # username : str
    # email : EmailStr
    hashed_password : str
    first_name: Optional[str] = None 
    last_name: Optional[str] = None
    disabled: Optional[bool] = None

    def __repr__(self) -> str:
        return f"<User {self.email}>"

    def __str__(self) -> str:
        # return self.email
        user_dict = {
            "user_id": f"{self.user_id}",
            "username": f"{self.username}",
            "email": f"{self.email}",
            "fast_name": f"{self.first_name}",
            "last_name": f"{self.last_name}",
            "disabled" : f"{self.disabled}"
        }
        return str(user_dict)

    def __hash__(self) -> int:
        return hash(self.email)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, User):
            return self.email == other.email
        return False
    
    @property
    def create(self) -> datetime:
        return self.id.generation_time
    
    @classmethod
    async def by_email(self, email: str) -> "User":
        return await self.find_one(self.email == email)
    

    # 设置索引
    """
    class Index:
        keys = [("email", 1), ("username", 1)]
        unique = True 
    """

    class Settings:
        name = "users"  # 指定集合名称   
