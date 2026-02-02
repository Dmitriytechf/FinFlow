from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class BaseSchema(BaseModel):
    '''Базовая схема со стандартной конфигурацией'''
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,  # Разрешить alias имена
    )


class TimestampMixin(BaseSchema):
    '''Миксин с полями времени'''
    created_at: datetime
    updated_at: datetime | None = None


class IDMixin(BaseSchema):
    '''Миксин с ID'''
    id: UUID


class BaseResponseSchema(IDMixin, TimestampMixin):
    '''Базовая схема для ответов API'''
    pass
