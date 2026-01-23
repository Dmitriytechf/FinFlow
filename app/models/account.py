from sqlalchemy import Column, String, Numeric, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Account(BaseModel):
    '''
    Модель счетов пользователя (кошелек, карта, депозит)
    '''
    __tablename__ = 'accounts'

    user_id = Column(
        UUID(as_uuid=True),
        # При удалении пользователя удаляем счета
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    # Название счета
    name = Column(
        String(64),
        nullable=False,
        default='Основной счет'
    )
    # Описание
    description = Column(
        String(255),
        nullable=True
    )
    # Баланс счета
    balance = Column(
        Numeric(10, 2),  # 10 цифр всего, 2 после запятой
        default=0.00,
        nullable=False
    )
    # Валюта счета
    currency = Column(
        String(3),  # RUB, USD, EUR, CNY
        default='RUB',
        nullable=False
    )
    # Тип счета: cash, bank_card
    account_type = Column(
        String(20),
        default='bank_card',
        nullable=False
    )
    # Активен ли счет (можно скрыть старые счета)
    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    # Связи
    user = relationship('User', back_populates='accounts')
    transactions = relationship('Transaction',
                                foreign_keys='Transaction.account_id',
                                back_populates='account', 
                                cascade='all, delete-orphan')
    goals = relationship('Goal', back_populates='account', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Account(id={self.id}, name={self.name}, balance={self.balance})>'
