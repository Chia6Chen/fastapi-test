from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.models.user_model import User
from app.api.v1 import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"---- Start up ....{settings.PROJECT_NAME}")
    # initialize crucial application services
    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING).fodoist
    
    await init_beanie(
        database=db_client,
        document_models= [
            User
        ]
    )

    yield
    print("----- Shutting down .....")

app =FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

app.include_router(router.router, prefix=settings.API_V1_STR)

@app.get('/')
async def hello():
    return {"message": "Hello world ..."}
