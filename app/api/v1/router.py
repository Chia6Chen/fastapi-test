from fastapi import APIRouter
from app.api.v1.handlers import user
from app.api.v1.handlers import todo
from app.api.auth import jwt


router = APIRouter()

router.include_router(user.user_router, prefix='/users', tags=["users"])
router.include_router(jwt.auth_router, prefix='/auth', tags=["auth"])
router.include_router(todo.todo_router, prefix='/todo', tags=['todo'])
