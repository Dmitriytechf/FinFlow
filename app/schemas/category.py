from uuid import UUID
from enum import Enum

from pydantic import Field

from .base import BaseSchema, BaseResponseSchema


class CategoryType(str, Enum):
    INCOME = 'income'    # Доходы
    EXPENSE = 'expense'  # Расходы


class CategoryBase(BaseSchema):
    '''Базовая схема категории'''
    name: str = Field(..., max_length=64, description='Название категории')
    type: CategoryType = Field(..., description='Доход/расход')


class CategoryCreate(CategoryBase):
    '''Создание категории'''
    parent_id: UUID | None = Field(None, description='ID родительской категории')


class CategoryUpdate(BaseSchema):
    '''Обновление категории'''
    name: str | None = Field(None, max_length=64)
    type: CategoryType | None = Field(None, description='Доход/расход')


class CategoryResponse(BaseResponseSchema):
    '''Ответ с данными категории'''
    user_id: UUID | None  # None для системных категорий
    name: str
    type: CategoryType
