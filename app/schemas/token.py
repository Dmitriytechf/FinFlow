from datetime import datetime

from .base import BaseSchema


class Token(BaseSchema):
    '''Схема JWT токена'''
    access_token: str
    refresh_token: str | None = None
    token_type: str = 'bearer'
    expires_at: datetime | None = None


class TokenPayload(BaseSchema):
    '''Полезная нагрузка JWT токена(decoded)'''
    sub: str  # subject (user_id)
    exp: int | None = None  # expiration time
    iat: int | None = None  # issued at
    email: str | None = None


class TokenData(BaseSchema):
    '''Данные из токена для внутреннего использования'''
    user_id: str
    email: str | None = None
