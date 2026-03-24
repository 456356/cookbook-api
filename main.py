from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import Base, engine
from routers import recipes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создание таблиц при старте приложения
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Здесь можно закрыть ресурсы, если нужно
    # await engine.dispose()


app = FastAPI(
    title="Cookbook API",
    description="API для кулинарной книги. "
    "Позволяет просматривать рецепты, создавать новые "
    "и отслеживать популярность по просмотрам.",
    version="1.0.0",
    contact={
        "name": "Student",
        "email": "student@example.com",
    },
    lifespan=lifespan,
)

app.include_router(recipes.router)


@app.get("/", tags=["root"])
async def root():
    return {"message": "Cookbook API. Перейдите к /docs для документации."}
