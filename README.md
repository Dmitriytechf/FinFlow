# FinFlow API

![FastAPI](https://img.shields.io/badge/FastAPI-0.104.0-009688?logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-✓-2496ED?logo=docker)


Личный финансовый менеджер с API интерфейсом. Учет доходов, расходов, аналитика и управление бюджетами.


## 🚀 Быстрый старт проекта

### Предварительные требования

- **Python 3.9+**
- **Docker & Docker Compose**
- **Make** (для Windows установить через Chocolatey)

### Установка и запуск

#### Вариант 1: С использованием Make (рекомендуется)

**1. Клонировать репозиторий**
```bash
git clone <repository-url>
cd finflow-api
```
**2. Создать виртуальное окружение**
```bash
make venv
```
**3. Активировать виртуальное окружение**
```bash
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```
**4. Установить зависимости**
```bash
make install
```
**5. Запустить Docker сервисы**
```bash
make docker-up
```
**6. Проверить работу**
```bash
curl http://localhost:8000/
```

#### Вариант 2: Без Make (ручная установка)
**1. Клонировать репозиторий**
```bash
git clone <repository-url>
cd finflow-api
```
**2. Создать и активировать виртуальное окружение**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# или source venv/bin/activate  # Linux/macOS
```
**3. Установить зависимости**
```bash
pip install -r requirements.txt
```
**4. Запустить Docker**
```bash
docker-compose up -d
```
**5. Применить миграции базы данных**
```bash
alembic upgrade head
```
**6. Запустить сервер**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Помощь командой:**
```bash
make help
```
