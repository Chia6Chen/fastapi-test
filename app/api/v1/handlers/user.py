from fastapi import APIRouter, HTTPException, status
from app.schemas.user_schemas import UserAuth, UserOut
from app.services.user_service import UserService
from beanie.exceptions import RevisionIdWasChanged
from pymongo.errors import DuplicateKeyError
from typing import List


user_router = APIRouter()

@user_router.get('/test')
async def test():
    return {"message": "user router working"}

@user_router.post('/create', summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth):
    try:
        user_data = await UserService.create_user(data)
        # print(str(user_data))
        return user_data
    
    except Exception as e:
        """
        in beanie/odm/documents.py
         except DuplicateKeyError:
            raise RevisionIdWasChanged
        """
        print(f"----------{type(e).__name__}")
        if type(e).__name__ == "RevisionIdWasChanged":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email or username already exist"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating user"
            )
    