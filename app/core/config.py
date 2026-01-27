from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    '''
    Конфигурация приложения через переменные окружения.
    Pydantic Settings для валидации
    '''
    SECRET_KEY: str
    # Общие настройки
    PROJECT_NAME: str = 'FinFlow API'
    VERSION: str = '1.0.0'
    DESCRIPTION: str = 'API для управления личными финансами'

    # Окружение
    ENVIRONMENT: str = 'development'  # development, staging, production
    DEBUG: bool = False

    # API
    API_PREFIX: str = '/api'
    API_V1_PREFIX: str = '/api/v1'
    HOST: str = '0.0.0.0'
    PORT: int = 8000
    RELOAD: bool = True

    # База данных PostgreSQL
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = 'localhost'
    POSTGRES_PORT: str = '5432'

    @property
    def DATABASE_URL(self) -> str:
        '''URL для подключения к PostgreSQL'''
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'

    @property
    def SYNC_DATABASE_URL(self) -> str:
        '''Синхронный URL для Alembic (psycopg2)'''
        return f'postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'

    # Redis (для кеша и Celery)
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: str = '6379'
    REDIS_DB: str = '0'

    @property
    def REDIS_URL(self) -> str:
        '''URL для подключения к Redis'''
        return f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}'

    @property
    def CELERY_BROKER_URL(self) -> str:
        '''URL брокера для Celery'''
        return self.REDIS_URL
    
    @property
    def CELERY_RESULT_BACKEND(self) -> str:
        '''Бэкенд для результатов Celery'''
        return self.REDIS_URL

    CORS_ORIGINS: list[str] = ['*'] # Только для разработки!

    class Config:
        '''
        Конфигурация Pydantic Settings:
        - Читать переменные из .env
        - Кодировка UTF-8
        '''
        env_file = '.env'
        env_file_encoding = 'utf-8'


# Создаем глобальный объект настроек
settings = Settings()
