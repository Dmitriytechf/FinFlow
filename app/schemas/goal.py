from uuid import UUID
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum

from pydantic import Field, computed_field

from .base import BaseSchema, BaseResponseSchema


class GoalStatus(str, Enum):
    ACTIVE = 'active'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    ON_HOLD = 'on_hold'


class GoalBase(BaseSchema):
    '''Базовая схема цели'''
    name: str = Field(..., description='Название цели')
    status: GoalStatus = Field(default=GoalStatus.ACTIVE, description='Статус цели')
    target_amount: Decimal = Field(..., gt=0, description='Целевая сумма')
    current_amount: Decimal = Field(0.00, ge=0, description='Текущая сумма')
    priority: int = Field(1, ge=1, le=99, description='Приоритет (1-99)')


class GoalCreate(GoalBase):
    '''Создание цели'''
    account_id: UUID | None = Field(None, description='ID счета для накопления')


class GoalUpdate(BaseSchema):
    '''Обновление цели'''
    name: str | None = Field(None, max_length=128)
    target_amount: Decimal | None = Field(None, gt=0)
    current_amount: Decimal | None = Field(None, ge=0)
    priority: int | None = Field(None, ge=1, le=99)
    account_id: UUID | None = None


class GoalResponse(BaseResponseSchema):
    '''Ответ с данными цели'''
    user_id: UUID
    account_id: UUID | None
    name: str
    target_amount: Decimal
    current_amount: Decimal
    priority: int
    status: GoalStatus

    # Вычисляемые поля (добавляем как свойства в response)
    @computed_field
    @property
    def progress_percent(self) -> float:
        '''Процент выполнения цели'''
        if self.target_amount == 0: # чтобы не было деления на 0
            return 0.0
        return float((self.current_amount / self.target_amount) * 100)

    @computed_field
    @property
    def  remaining_amount(self) -> Decimal:
        '''Осталось накопить'''
        remaining = self.target_amount - self.current_amount
        result = max(remaining, Decimal('0.00')) # Decimal для точности
        # Округляем ответ до 2 знаков
        return result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


class GoalStatusUpdate(BaseSchema):
    '''Изменение статуса цели'''
    status: GoalStatus | None = None


class GoalDeposit(BaseSchema):
    '''Пополнение цели'''
    amount: Decimal = Field(..., gt=0, description="Сумма пополнения")
    description: str | None = Field(None, description='Описание')


class GoalAnalytics(BaseSchema):
    '''Аналитика по целям'''
    total_goals: int
    active_goals: int
    completed_goals: int
    total_target_amount: Decimal
    total_current_amount: Decimal
    total_progress_percent: float
    total_remaining_amount: Decimal
