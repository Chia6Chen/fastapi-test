from app.schemas.user_schemas import UserAuth
from app.models.user_model import User
from app.core.security import get_password, verify_password
from typing import Optional
from uuid import UUID


class UserService:
    @staticmethod
    async def create_user(user: UserAuth):
        user_in = User(
            username=user.username,
            email=user.email,
            hashed_password=get_password(user.password)
        )
        await user_in.save()
        return user_in
    
    @staticmethod
    async def authenticate(email: str, password: str) -> Optional[User]:
        user = await UserService.get_user_by_email(email=email)

        user_dict = {
            "user_id": f"{user.user_id}",
            "username": f"{user.username}",
            "email": f"{user.email}",
            "hasded_password": f"{user.hashed_password}",
            "fast_name": f"{user.first_name}",
            "last_name": f"{user.last_name}",
            "disabled" : f"{user.disabled}"
        }
        print(str(user_dict))

        if not user:
            return None
        if not verify_password(password=password, hashed_password=user.hashed_password):
            return None
        return user

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        user = await User.find_one(User.email == email) 
        # user = User.by_email(email)
        return user

    @staticmethod
    async def get_user_by_id(id: UUID) -> Optional[User]:
        user = await User.find_one(User.id == id) 
        return user
