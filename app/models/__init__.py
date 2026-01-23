from app.models.base import BaseModel
from app.core.database import Base
from app.models.user import User
from app.models.account import Account
from app.models.category import Category, CategoryType
from app.models.transaction import Transaction, TransactionType
from app.models.goal import Goal, GoalStatus


# Удобный импорт:
#  from app.models import User, Goal, Transaction
# Полный импорт всего:
#  from app.models import *

__all__ = [
    'Base', 'BaseModel',
    'User',
    'Account',
    'Category', 'CategoryType',
    'Transaction', 'TransactionType',
    'Goal', 'GoalStatus'
]
