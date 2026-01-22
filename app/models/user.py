from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class User(BaseModel):
    '''
    Пользователь системы
    '''
    __tablename__ = 'users'  # Имя таблицы в БД

    # Обязательные поля
    email = Column(
        String(128),
        unique=True,  # Email должен быть уникальным
        index=True,   # Индекс для быстрого поиска
        nullable=False
    )
    
    hashed_password = Column(
        String(128),
        nullable=False  # Пароль обязателен
    )

    # Дополнительные поля
    name = Column(
        String(64),
        nullable=True
    )

    def __repr__(self):
        '''
        Представление объекта для отладки
        '''
        return f'<User(id={self.id}, name={self.name}, email={self.email})>'
