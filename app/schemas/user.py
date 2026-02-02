from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, validator, ConfigDict
from .base import BaseSchema, BaseResponseSchema


class UserRegister(BaseSchema):
    '''Регистрация нового пользователя'''
    email: EmailStr = Field(..., description='Email пользователя')
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description='Пароль (минимум 8 символов, заглавная буква, цифра)'
    )
    name: str | None = Field(
        None,
        max_length=64,
        description='Имя пользователя (опционально)'
    )

    @validator('password')
    def validate_user_password(cls, v: str) -> str:
        '''Валидация сложности пароля'''
        if len(v) < 8:
            raise ValueError('Пароль должен быть не менее 8 символов')
        if not any(c.isupper() for c in v):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву')
        if not any(c.isdigit() for c in v):
            raise ValueError('Пароль должен содержать хотя бы одну цифру')
        return v
    
    @validator('email')
    def email_to_lowercase(cls, v: str) -> str:
        '''Приводим email к нижнему регистру'''
        return v.lower()


class UserLogin(BaseSchema):
    '''Вход в систему'''
    email: EmailStr = Field(..., description='Email')
    password: str = Field(..., description='Пароль')
    remember_me: bool = Field(False, description='Больше срок токена')


class UserUpdate(BaseSchema):
    '''Обновление данных пользователя'''
    name: str | None = Field(None, max_length=64)


class UserChangePassword(BaseSchema):
    """Смена пароля"""
    current_password: str = Field(..., description='Текущий пароль')
    new_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description='Новый пароль'
    )

    @validator('new_password')
    def validate_new_password(cls, v: str, values: dict) -> str:
        """Валидация нового пароля"""
        if len(v) < 8:
            raise ValueError('Новый пароль должен быть не менее 8 символов')
        if not any(c.isupper() for c in v):
            raise ValueError('Новый пароль должен содержать заглавную букву')
        if not any(c.isdigit() for c in v):
            raise ValueError('Новый пароль должен содержать цифру')
        if 'current_password' in values and v == values['current_password']:
            raise ValueError('Новый пароль должен отличаться от текущего')

        return v


# Ответы клиенту
class UserResponse(BaseResponseSchema):
    '''Ответ с данными пользователя'''
    email: EmailStr
    name: str | None
    
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': '123e4567-e89b-12d3-a456-426333174000',
                'email': 'user@example.com',
                'name': 'Дарт Вейдер',
                'created_at': '2026-01-15T10:30:00Z',
                'updated_at': '2026-01-15T10:30:00Z'
            }
        }
    )


# Для внутреннего использования
class UserInDB(BaseSchema):
    '''Пользователь в БД (с хешированным паролем)'''
    id: UUID
    email: EmailStr
    name: str | None
    hashed_password: str
    created_at: datetime
    updated_at: datetime | None
