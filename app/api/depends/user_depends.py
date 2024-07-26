from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from fastapi import Depends, HTTPException, status
from app.models.user_model import User
from app.schemas.auth_schemas import TokenPayload
from app.services.user_service import UserService

from jose import jwt
from datetime import datetime
from pydantic import ValidationError
from uuid import UUID


reuseable_oauth = OAuth2PasswordBearer (
    tokenUrl = f"{settings.API_V1_STR}/auth/login",
    scheme_name="JWT"
)

async def get_current_user(token: str = Depends(reuseable_oauth)) -> User: 
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        # print(f"token_data.exp = {datetime.fromtimestamp(int(token_data.exp))}, ---{datetime.now()}")

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
    
    # print(f"-----token_data.sub = {token_data.sub}, {type(token_data.sub)}")
    # user = await UserService.get_user_by_id(token_data.sub)
    user = await User.find_one(User.user_id == token_data.sub)
    if not user:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="could not find user"
            )
    return user
