from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any

from app.services.user_service import UserService
from app.core.security import create_access_token, create_refresh_token
from app.core.security import get_password
from app.schemas.auth_schemas import TokenSchemas
from app.schemas.user_schemas import UserOut
from app.api.depends.user_depends import get_current_user
from app.models.user_model import User


auth_router = APIRouter()

@auth_router.post("/login", summary="create access and refresh token for user", 
                  response_model=TokenSchemas)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = await UserService.authenticate(email=form_data.username, 
                                          password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    return {
        "access_token": create_access_token(user.user_id),
        "refresh_token": create_refresh_token(user.user_id)
    }
     
@auth_router.post("/test-token", summary="test if the access token is valid", 
                  response_model=UserOut)
async def test_token(user: User = Depends(get_current_user)):
    return user
