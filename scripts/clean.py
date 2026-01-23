import os
import shutil
import glob


def clean_directory():
    print('Удаление __pycache__ папок...')
    # Рекурсивно ищем и удаляем __pycache__
    for root, dirs, _ in os.walk('.'):
        for d in dirs:
            if d == '__pycache__':
                path = os.path.join(root, d)
                try:
                    shutil.rmtree(path)
                    print(f'  Удалено: {path}')
                except:
                    pass

    print('Удаление .pyc и .pyo файлов...')
    # Рекурсивно ищем и удаляем .pyc/.pyo файлы
    for root, _, files in os.walk('.'):
        for f in files:
            if f.endswith('.pyc') or f.endswith('.pyo'):
                path = os.path.join(root, f)
                try:
                    os.remove(path)
                    print(f'  Удалено: {path}')
                except:
                    pass
    # Удаляем другие временные файлы/папки
    items_to_remove = [
        '.pytest_cache',
        '.mypy_cache', 
        '.cache',
        'build',
        'dist',
        '.coverage'
    ]

    for item in items_to_remove:
        if os.path.exists(item):
            try:
                if os.path.isfile(item):
                    os.remove(item)
                else:
                    shutil.rmtree(item)
                print(f'Удалено: {item}')
            except:
                pass

    # Удаляем все *.egg-info папки
    for egg_info in glob.glob('*.egg-info'):
        if os.path.exists(egg_info):
            try:
                shutil.rmtree(egg_info)
                print(f'Удалено: {egg_info}')
            except:
                pass

    print('Очистка завершена!')


if __name__ == '__main__':
    clean_directory()
