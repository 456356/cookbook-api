from typing import List

from pydantic import BaseModel, ConfigDict, Field


class RecipeBase(BaseModel):
    title: str = Field(..., description="Название блюда", min_length=1)

    cooking_time: int = Field(..., description="Время приготовления в минутах", gt=0)

    ingredients: List[str] = Field(..., description="Список ингредиентов")

    description: str = Field(..., description="Пошаговое описание приготовления")


class RecipeCreate(RecipeBase):
    pass


class Recipe(RecipeBase):
    id: int
    views: int
    model_config = ConfigDict(from_attributes=True)


class RecipeListItem(BaseModel):
    title: str
    views: int
    cooking_time: int
    model_config = ConfigDict(from_attributes=True)
