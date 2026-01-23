.PHONY: help venv install dev test docker-up docker-down docker-build \
        logs-api logs-celerybeat logs-celeryworker db-shell redis-cli \
        migrate migrate-up migrate-down clean mini-reset reset


help: ## Показать помощь
	@echo "FinFlow API - Management Commands"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "${GREEN}%-20s${NC} %s\n", $$1, $$2}'
	@echo "^-^"

venv: ## Создать виртуальное окружение
	@echo "Creating virtual environment..."
	python -m venv venv
	@echo "Virtual environment created"
	@echo "To activate:"
	@echo "  Linux/macOS: source venv/bin/activate"
	@echo "  Windows:     venv\\Scripts\\activate"

install: ## Установить основные зависимости
	@echo "Installing main dependencies..."
	pip install -r requirements.txt
	@echo "Main dependencies installed"

dev: ## Запустить сервер для разработки
	@echo "Starting development server..."
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test: ## Запустить тесты
	@echo "Running tests..."
	pytest -v

docker-up: ## Запустить все сервисы в Docker
	@echo "Starting Docker Compose..."
	docker-compose up -d
	@echo "✓ Services started"
	@echo "API: http://localhost:8000"
	@echo "Docs: http://localhost:8000/docs"

docker-down: ## Остановить Docker Compose
	@echo "Stopping Docker Compose..."
	docker-compose down

docker-build: ## Пересобрать Docker образы
	@echo "Rebuilding Docker images..."
	docker-compose build --no-cache

logs-api: ## Показать логи API
	@echo "API logs:"
	docker-compose logs -f api

logs-celerybeat: ## Показать логи celery-beat
	@echo "Celery beat logs:"
	docker-compose logs -f celery-beat

logs-celeryworker: ## Показать логи celery-worker
	@echo "Celery worker logs:"
	docker-compose logs -f celery-worker

db-shell: ## Открыть shell в PostgreSQL
	@echo "Connecting to PostgreSQL..."
	docker-compose exec postgres psql

redis-cli: ## Открыть Redis CLI
	@echo "Connecting to Redis..."
	docker-compose exec redis redis-cli

migrate: ## Создать миграцию (использовать: make migrate m="описание")
	@echo "Creating migration..."
	alembic revision --autogenerate -m "$(m)"

migrate-up: ## Применить миграции
	@echo "Applying migrations..."
	alembic upgrade head

migrate-down: ## Откатить миграцию
	@echo "Rolling back migration..."
	alembic downgrade -1

clean: ## Очистить временные файлы и папки __pycache__
	python scripts/clean.py

mini-reset: ## Пересборка контейнеров
	@echo "Recreating project..."
	docker-compose down
	docker-compose build
	docker-compose up -d
	@echo "Waiting for services to start..."
	sleep 5
	alembic upgrade head
	@echo "✓ Project built"

reset: ## Полный сброс (остановить, удалить volumes, пересобрать)
	@echo "WARNING: Full project reset"
	@echo "This will delete all data in the database!"
	docker-compose down -v
	docker-compose build --no-cache
	docker-compose up -d
	sleep 5
	alembic upgrade head
	@echo "✓ Project reset and restarted"
