import uuid
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.core.database import Base


class BaseModel(Base):
    '''
    Абстрактная базовая модель с общими полями
    Все другие модели наследуются от нее
    '''
    __abstract__ = True  # Не создавать таблицу для этой модели

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(), # Время создания записи
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),  # Автоматически обновлять при изменении
        nullable=False
    )
