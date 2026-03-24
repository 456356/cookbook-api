from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import crud
import schemas
from database import get_db

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.get(
    "/",
    response_model=List[schemas.RecipeListItem],
    summary="Список всех рецептов",
    description=(
        "Возвращает список рецептов, отсортированных по убыванию просмотров, "
        "а при равных просмотрах — по возрастанию времени приготовления."
    ),
)
async def read_recipes(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),  # noqa: B008
):
    return await crud.get_recipes(db, skip=skip, limit=limit)


@router.get(
    "/{recipe_id}",
    response_model=schemas.Recipe,
    summary="Детальная информация о рецепте",
    description="При каждом вызове увеличивает счётчик просмотров рецепта.",
)
async def read_recipe(
    recipe_id: int,
    db: AsyncSession = Depends(get_db),  # noqa: B008
):
    # Проверяем существование рецепта
    recipe = await crud.get_recipe(db, recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    # Увеличиваем просмотры
    await crud.increment_views(db, recipe_id)

    # Возвращаем обновлённые данные (повторно читаем из БД)
    return await crud.get_recipe(db, recipe_id)


@router.post(
    "/",
    response_model=schemas.Recipe,
    status_code=201,
    summary="Создать новый рецепт",
    description=(
        "Добавляет рецепт в базу. " "Поле views автоматически устанавливается в 0."
    ),
)
async def create_recipe(
    recipe: schemas.RecipeCreate,
    db: AsyncSession = Depends(get_db),  # noqa: B008
):
    return await crud.create_recipe(db, recipe)
