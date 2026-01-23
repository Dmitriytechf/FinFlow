import enum
from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy import Column, String, Numeric, ForeignKey, DateTime, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class GoalStatus(enum.Enum):
    '''Статус цели'''
    ACTIVE = 'active'      # Активна (копим)
    COMPLETED = 'completed' # Достигнута
    CANCELLED = 'cancelled' # Отменена
    ON_HOLD = 'on_hold'    # На паузе


class Goal(BaseModel):
    '''
    Цель накопления
    '''
    __tablename__ = 'goals'

    # Связь с пользователем
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )

    # Связь со счетом. На каком счете копить
    account_id = Column(
        UUID(as_uuid=True),
        ForeignKey('accounts.id', ondelete='SET NULL'),
        nullable=True,
        index=True
    )

    name = Column(
        String(128),
        nullable=False
    )

    target_amount = Column(
        Numeric(10, 2),  # Целевая сумма
        nullable=False
    )
    
    current_amount = Column(
        Numeric(10, 2),  # Текущая накопленная сумма
        default=0.00,
        nullable=False
    )

    status = Column(
        Enum(GoalStatus),
        default=GoalStatus.ACTIVE,
        nullable=False,
        index=True
    )

    priority = Column(
        Numeric(2, 0),  # От 1 до 99
        default=5,
        nullable=False
    )

    @property
    def progress_percent(self) -> float:
        '''Процент выполнения цели'''
        if self.target_amount == 0:
            return 0.0
        return (self.current_amount / self.target_amount) * 100

    @property
    def remaining_amount(self) -> Decimal:
        '''
        Осталось накопить

        Returns:
            Decimal: Сумма, которую осталось накопить, 
                    округленная до 2 знаков (минимум 0.00)
        '''
        result = max(self.target_amount - self.current_amount, Decimal('0.00'))
        return result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    # Связи
    user = relationship('User', back_populates='goals')
    account = relationship('Account', back_populates='goals')

    def __repr__(self):
        return f'<Goal(id={self.id}, name={self.name}>'
