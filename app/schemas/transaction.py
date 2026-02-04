from uuid import UUID
from decimal import Decimal
from datetime import datetime, timezone

from enum import Enum
from pydantic import Field, field_validator, ConfigDict

from .base import BaseSchema, BaseResponseSchema


class TransactionType(str, Enum):
    INCOME = 'income'      # Доход (деньги ПРИШЛИ)
    EXPENSE = 'expense'    # Расход (деньги УШЛИ)
    TRANSFER = 'transfer'  # Перевод между счетами


class TransactionBase(BaseSchema):
    '''Базовая схема транзакции'''
    type: TransactionType = Field(..., description='Тип транзакции')
    amount: Decimal = Field(..., gt=0, description='Сумма транзакции')
    description: str | None = Field(None, description='Описание транзакции')
    tags: list[str] | None = Field(None, description='Теги')
    transaction_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description='Дата совершения транзакции'
    )


class TransactionCreate(TransactionBase):
    '''Создание транзакции'''
    account_id: UUID = Field(..., description='ID счета')
    category_id: UUID | None = Field(None, description='ID категории')
    to_account_id: UUID | None = Field(
        None,
        description='ID счета-получателя (для переводов)'
    )

    @field_validator('to_account_id')
    @classmethod
    def validate_transfer(cls, v, values):
        '''Валидация для переводов'''
        if values.get('type') == TransactionType.TRANSFER and not v:
            raise ValueError('Для перевода обязательно указать счет-получатель')
        if values.get('type') != TransactionType.TRANSFER and v:
            raise ValueError('Счет-получатель указывается только для переводов')
        return v

    @field_validator('category_id')
    @classmethod
    def validate_category_id(cls, v, values):
        '''Валидация категории'''
        if v and values.get('type') == TransactionType.TRANSFER:
            raise ValueError('Для переводов не указывается категория')
        return v


class TransactionUpdate(BaseSchema):
    '''Обновление транзакции'''
    amount: Decimal | None = Field(None, gt=0)
    description: str | None = None
    transaction_date: datetime | None= None
    tags: list[str] | None = None
    category_id: UUID | None = None


class TransactionResponse(BaseResponseSchema):
    '''Ответ с данными транзакции'''
    user_id: UUID
    account_id: UUID
    category_id: UUID | None
    to_account_id: UUID | None
    amount: Decimal
    type: TransactionType
    description: str | None
    transaction_date: datetime
    tags: list[str] | None

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': '123e4567-e89b-12d3-a456-426614174000',
                'user_id': '123e4567-e89b-12d3-a456-426614174001',
                'account_id': '123e4567-e89b-12d3-a456-426614174002',
                'amount': 999.99,
                'type': 'expense',
                'description': 'Новый телефон',
                'transaction_date': '2026-01-15T14:30:00Z',
                'tags': ['техника', 'смартфон'],
                'created_at': '2026-01-15T14:35:00Z',
                'updated_at': '2026-01-15T14:35:00Z'
            }
        }
    )


# Специальные схемы для операций
class TransferCreate(BaseSchema):
    '''Создание перевода между счетами'''
    from_account_id: UUID = Field(..., description='ID счета-отправителя')
    to_account_id: UUID = Field(..., description='ID счета-получателя')
    amount: Decimal = Field(..., gt=0, description='Сумма перевода')
    description: str | None = Field(None, description='Описание')

    @field_validator('to_account_id')
    @classmethod
    def different_accounts(cls, v, values):
        '''Нельзя переводить на тот же счет'''
        if ('from_account_id' in values.data and
            v == values.data['from_account_id']):
            raise ValueError('Нельзя переводить на тот же счет')
        return v


class TransactionFilter(BaseSchema):
    '''Фильтр для поиска транзакций'''
    type: TransactionType | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    min_amount: Decimal | None = None
    max_amount: Decimal | None = None
    tags: list[str] | None = None


class TransactionAnalytics(BaseSchema):
    '''Аналитика по транзакциям'''
    total_income: Decimal
    total_expense: Decimal
    total_transfers: Decimal
