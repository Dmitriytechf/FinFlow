from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings


# Базовый класс для всех моделей
Base = declarative_base()

# Создаем движок для подключения к БД
engine = create_async_engine(
    settings.DATABASE_URL,
    # Показывать SQL запросы только в development
    echo=settings.ENVIRONMENT == 'development',
    pool_pre_ping=True,  # Проверять соединение перед использованием
)

# Создаем фабрику сессий для работы с БД
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False, # Не удалять объекты после коммита
    autocommit=False,
    autoflush=False,
)


async def get_db():
    '''
    Зависимость для FastAPI - предоставляет сессию БД
    '''
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
