from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
from jose import jwt
from datetime import datetime
from pydantic import ValidationError

from app.services.user_service import UserService
from app.core.security import create_access_token, create_refresh_token
from app.core.security import get_password
from app.schemas.auth_schemas import TokenSchemas, TokenPayload
from app.schemas.user_schemas import UserOut
from app.api.depends.user_depends import get_current_user
from app.models.user_model import User
from app.core.config import settings


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

@auth_router.post("/refresh", summary="Refresh token", response_model=TokenSchemas)
async def refresh_token(refresh_token: str = Body(...)):
    try:
        payload = jwt.decode(
            refresh_token, settings.JWT_REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        print(f"token_data.exp = {datetime.fromtimestamp(int(token_data.exp))}, ---{datetime.now()}")

        if datetime.fromtimestamp(int(token_data.exp)) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="token expired",
                headers={"WWW-Authenticate": "Bearer"}
            )
    except(jwt.JWTError, ValidationError) as e:
        print(str(e))
        raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )
    
    print(f"-----token_data.sub = {token_data.sub}, {type(token_data.sub)}")
    # user = await UserService.get_user_by_id(token_data.sub)
    user = await User.find_one(User.user_id == token_data.sub)
    if not user:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="could not find user"
            )
    return {
        "access_token": create_access_token(user.user_id),
        "refresh_token": create_refresh_token(user.user_id),
    }
