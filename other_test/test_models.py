import sys
from pathlib import Path

# Получаем абсолютный путь к корню проекта
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import asyncio

from app.models.user import User



async def test_user_model():
    user = User(
        email='test@example.com',
        hashed_password='hashed_password_here',
        name='Test User'
    )
    
    print(f'Создан пользователь: {user}')
    print(f'{user.email=}')
    print(f'{user.name=}')


if __name__ == '__main__':
    asyncio.run(test_user_model())
