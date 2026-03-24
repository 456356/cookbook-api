import pytest
from fastapi.testclient import TestClient
import asyncio
from main import app
from database import engine, Base

client = TestClient(app)

# Функция, которая выполнится один раз перед всеми тестами
def setup_module(module):
    """Создаёт таблицы в базе данных перед запуском тестов."""
    async def create_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    asyncio.run(create_tables())

def teardown_module(module):
    """Опционально: удаляет таблицы после всех тестов."""
    async def drop_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
    asyncio.run(drop_tables())

def test_create_recipe():
    payload = {
        "title": "Омлет",
        "cooking_time": 10,
        "ingredients": ["яйца", "молоко"],
        "description": "Взбить и пожарить"
    }
    response = client.post("/recipes/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["views"] == 0
    assert "id" in data

def test_get_recipes_list():
    response = client.get("/recipes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_recipe_detail():
    # Создаём рецепт
    create_resp = client.post("/recipes/", json={
        "title": "Для детального",
        "cooking_time": 15,
        "ingredients": ["ингр"],
        "description": "описание"
    })
    recipe_id = create_resp.json()["id"]

    # Получаем детали
    response = client.get(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == recipe_id
    assert data["views"] == 1

def test_get_nonexistent_recipe():
    response = client.get("/recipes/99999")
    assert response.status_code == 404

