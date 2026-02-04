from uuid import UUID
from decimal import Decimal

from pydantic import Field

from .base import BaseSchema, BaseResponseSchema


class AccountBase(BaseSchema):
    '''Базовая схема для счета'''
    name: str = Field(
        ...,
        max_length=64,
        description='Название счета'
    )
    description: str | None = Field(
        None,
        max_length=255
    )
    currency: str = Field(
        'RUB',
        pattern='^[A-Z]{3}$',
        description='Валюта: RUB, USD, EUR, CNY, JPY'
    )
    account_type: str = Field(
        'bank_card',
        description='Тип: cash, bank_card'
    )
    is_active: bool = Field(
        True,
        description='Активен ли счет'
    )


class AccountCreate(AccountBase):
    '''Создание счета'''
    initial_balance: Decimal = Field(0.00, ge=0, description='Начальный баланс')


class AccountUpdate(BaseSchema):
    '''Обновление счета'''
    name: str | None = Field(None, max_length=64)
    description: str | None = Field(None, max_length=255)


class AccountResponse(BaseResponseSchema):
    """Ответ с данными счета"""
    user_id: UUID
    name: str
    description: str | None
    balance: Decimal
    currency: str
    account_type: str
    is_active: bool


class AccountBalanceUpdate(BaseSchema):
    '''Изменение баланса счета'''
    amount: Decimal = Field(..., description='Сумма изменения')
    description: str | None = Field(None, description="Описание операции")
