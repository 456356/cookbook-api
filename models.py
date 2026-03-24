from sqlalchemy import Column, Integer, String, Text

from database import Base, JsonType


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False, comment="Название блюда")

    cooking_time = Column(
        Integer, nullable=False, comment="Время приготовления (минуты)"
    )

    ingredients = Column(
        JsonType, nullable=False, comment="Список ингредиентов в формате JSON"
    )

    description = Column(Text, nullable=False, comment="Описание приготовления")

    views = Column(Integer, default=0, comment="Количество просмотров")
