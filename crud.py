from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

import schemas
from models import Recipe


async def get_recipes(db: AsyncSession, skip: int = 0, limit: int = 100):
    """Получить список рецептов с сортировкой по просмотрам и времени."""
    result = await db.execute(
        select(Recipe)
        .order_by(Recipe.views.desc(), Recipe.cooking_time)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_recipe(db: AsyncSession, recipe_id: int):
    """Получить один рецепт по ID."""
    result = await db.execute(select(Recipe).where(Recipe.id == recipe_id))
    return result.scalar_one_or_none()


async def increment_views(db: AsyncSession, recipe_id: int):
    """Атомарно увеличить счётчик просмотров."""
    await db.execute(
        update(Recipe).where(Recipe.id == recipe_id).values(views=Recipe.views + 1)
    )
    await db.commit()


async def create_recipe(db: AsyncSession, recipe: schemas.RecipeCreate):
    """Создать новый рецепт (просмотры = 0)."""
    db_recipe = Recipe(
        title=recipe.title,
        cooking_time=recipe.cooking_time,
        ingredients=recipe.ingredients,
        description=recipe.description,
        views=0,
    )
    db.add(db_recipe)
    await db.commit()
    await db.refresh(db_recipe)
    return db_recipe
