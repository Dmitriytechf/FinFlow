import os
import shutil


def clean_directory():
    print(' Удаление __pycache__ папок...')
    pycache_count = 0
    # Рекурсивно ищем и удаляем __pycache__
    for root, dirs, _ in os.walk('.'): # рекурсивно обходим все папки, начиная с текущей
        for d in dirs:
            if d == '__pycache__':
                path = os.path.join(root, d)
                try:
                    shutil.rmtree(path) # удаляет папку со всем содержимым
                    pycache_count += 1
                    print(f'  Удалено: {path}')
                except:
                    pass
    print(f' Удалено __pycache__: {pycache_count}', '\n' , '-' * 25, '\n')

    print(' Удаление .pyc  файлов...')
    pyc_count = 0
    # Рекурсивно ищем и удаляем .pyc файлы
    for root, _, files in os.walk('.'):
        for f in files:
            if f.endswith('.pyc'):
                path = os.path.join(root, f)
                try:
                    os.remove(path) # удаляем файлы
                    pyc_count += 1
                    print(f'  Удалено: {path}')
                except:
                    pass
    print(f' Удалено файлов .pyc: {pyc_count}', '\n' , '-' * 25, '\n')

    # Удаляем другие временные файлы/папки
    items_to_remove = [
        '.pytest_cache',
        '.mypy_cache', 
        '.cache',
        'build',
        'dist',
        '.coverage'
    ]
    temp_count = 0
    for item in items_to_remove:
        if os.path.exists(item): # проверяем существование файла/папки
            try:
                if os.path.isfile(item): # проверяем, является ли путь файлом
                    os.remove(item)
                else:
                    shutil.rmtree(item)
                temp_count += 1
                print(f'Удалено: {item}')
            except:
                pass
    print(f' Удалено временных элементов: {temp_count}', '\n' , '-' * 25, '\n')

    print(' Очистка завершена!')


if __name__ == '__main__':
    clean_directory()
