from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.mongodb import MongoDB
from src.infrastructure.user_repository_impl import UserRepositoryImpl
from src.usecase.user_interactor import UserInteractor
from src.interfaces.api.user_controller import create_user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await MongoDB.connect()
    yield
    # Shutdown
    await MongoDB.disconnect()


app = FastAPI(
    title="CRUD Service",
    description="CRUD сервис на FastAPI",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация зависимостей
user_repository = UserRepositoryImpl()
user_interactor = UserInteractor(user_repository)

# Подключение роутеров
app.include_router(create_user_router(user_interactor))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
