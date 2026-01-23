import enum

from sqlalchemy import Column, String, ForeignKey, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class CategoryType(enum.Enum):
    INCOME = 'income'    # Доходы
    EXPENSE = 'expense'  # Расходы


class Category(BaseModel):
    '''
    Категория для транзакций (доходы/расходы)

    Примеры: Еда, Транспорт, Зарплата, Развлечения
    '''
    __tablename__ = 'categories'

    # Внешний ключ на пользователя
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=True,  # NULL = системная категория
        index=True
    )
    # Название категории
    name = Column(
        String(64),
        nullable=False
    )
    # Тип категории (доход/расход)
    type = Column(
        Enum(CategoryType),
        default=CategoryType.EXPENSE,
        nullable=False
    )
    # Иерархия: родительская категория
    parent_id = Column(
        UUID(as_uuid=True),
        ForeignKey('categories.id', ondelete='SET NULL'),
        nullable=True,
        index=True
    )

    # Связи
    user = relationship('User', back_populates='categories')
    parent = relationship('Category', remote_side='Category.id', back_populates='children')
    children = relationship('Category', back_populates='parent')

    def __repr__(self):
        return f'<Category(id={self.id}, name={self.name}, type={self.type.value})>'
