import enum
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import Column, String, Numeric, ForeignKey, DateTime, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class TransactionType(enum.Enum):
    '''
    Тип транзакции
    '''
    INCOME = 'income'      # Доход (деньги ПРИШЛИ)
    EXPENSE = 'expense'    # Расход (деньги УШЛИ)
    TRANSFER = 'transfer'  # Перевод между счетами


class Transaction(BaseModel):
    '''
    Транзакция - любая денежная операция между счетами.
    Поддерживает только ручной ввод.

    Включает в себя: доходы, расходы или переводы между счетами.
    '''
    __tablename__ = 'transactions'

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    account_id = Column(
        UUID(as_uuid=True),
        ForeignKey('accounts.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    category_id = Column(
        UUID(as_uuid=True),
        ForeignKey('categories.id', ondelete='SET NULL'),
        nullable=True,  # Может быть без категории
        index=True
    )
    # Для переводов: счет-получатель
    to_account_id = Column(
        UUID(as_uuid=True),
        ForeignKey('accounts.id', ondelete='SET NULL'),
        nullable=True,
        index=True
    )
    # Данные транзации
    type = Column(
        Enum(TransactionType),
        nullable=False,
        index=True
    )
    amount = Column(
        Numeric(10, 2),  # 10 цифр всего, 2 после запятой
        nullable=False
    )
    # Дата совершения транзакции (может отличаться от created_at)
    transaction_date = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True
    )
    description = Column(
        Text,
        nullable=True
    )
    # Теги для гибкой категоризации (например: работа, отпуск, хобби)
    tags = Column(
        String(64),
        nullable=True
    )

    # Связи
    user = relationship('User', back_populates='transactions')
    account = relationship('Account', foreign_keys=[account_id], back_populates='transactions')
    to_account = relationship('Account', foreign_keys=[to_account_id])
    category = relationship('Category', back_populates='transactions')

    def __repr__(self):
        return f'<Transaction(id={self.id}, type={self.type.value}, amount={self.amount})>'
