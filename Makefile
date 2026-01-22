.PHONY: help install dev test format lint docker-up docker-down logs

GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
NC := \033[0m


help: ## Показать помощь
	@echo "${YELLOW}FinFlow API - Команды управления${NC}"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "${GREEN}%-20s${NC} %s\n", $$1, $$2}'
	@echo "^-^"

venv: ## Создать виртуальное окружение
	@echo "${YELLOW}Создание виртуального окружения...${NC}"
	python -m venv venv
	@echo "${GREEN}Виртуальное окружение создано${NC}"
	@echo "Для активации:"
	@echo "  Linux/macOS: source venv/bin/activate"
	@echo "  Windows:     venv\\Scripts\\activate"

install: ## Установить основные зависимости
	@echo "${YELLOW}Установка основных зависимостей...${NC}"
	pip install -r requirements.txt
	@echo "${GREEN}Основные зависимости установлены${NC}"

dev: ## Запустить сервер для разработки
	@echo "${YELLOW}Запуск сервера разработки...${NC}"
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test: ## Запустить тесты
	@echo "${YELLOW}Запуск тестов...${NC}"
	pytest -v

docker-up: ## Запустить все сервисы в Docker
	@echo "${YELLOW}Запуск Docker Compose...${NC}"
	docker-compose up -d
	@echo "${GREEN}✓ Сервисы запущены${NC}"
	@echo "API: http://localhost:8000"
	@echo "Docs: http://localhost:8000/docs"

docker-down: ## Остановить Docker Compose
	@echo "${YELLOW}Остановка Docker Compose...${NC}"
	docker-compose down

docker-build: ## Пересобрать Docker образы
	@echo "${YELLOW}Пересборка Docker образов...${NC}"
	docker-compose build --no-cache

logs-api: ## Показать логи API
	@echo "${YELLOW}Логи API:${NC}"
	docker-compose logs -f api

logs-celerybeat: ## Показать логи celery-beat
	@echo "${YELLOW}Логи Сelery beat:${NC}"
	docker-compose logs -f celery-beat

logs-celeryworker: ## Показать логи celery-worker
	@echo "${YELLOW}Логи Celery worker:${NC}"
	docker-compose logs -f celery-worker

db-shell: ## Открыть shell в PostgreSQL
	@echo "${YELLOW}Подключение к PostgreSQL...${NC}"
	docker-compose exec postgres psql

redis-cli: ## Открыть Redis CLI
	@echo "${YELLOW}Подключение к Redis...${NC}"
	docker-compose exec redis redis-cli

migrate: ## Создать миграцию (использовать: make migrate m="описание")
	@echo "${YELLOW}Создание миграции...${NC}"
	alembic revision --autogenerate -m "$(m)"

migrate-up: ## Применить миграции
	@echo "${YELLOW}Применение миграций...${NC}"
	alembic upgrade head

migrate-down: ## Откатить миграцию
	@echo "${YELLOW}Откат миграции...${NC}"
	alembic downgrade -1

clean: ## Очистить временные файлы
	@echo "${YELLOW}Очистка временных файлов...${NC}"
ifeq ($(OS),Windows_NT)
	@echo "Windows - удаление кэша..."
	rmdir /s /q __pycache__ 2>nul || true
	rmdir /s /q app\__pycache__ 2>nul || true
	rmdir /s /q tests\__pycache__ 2>nul || true
	del /q *.pyc 2>nul || true
	del /q app\*.pyc 2>nul || true
	del /q tests\*.pyc 2>nul || true
	rmdir /s /q .pytest_cache 2>nul || true
	rmdir /s /q .mypy_cache 2>nul || true
	del /q .coverage 2>nul || true
else
	@echo "Linux/macOS - удаление кэша..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .coverage .pytest_cache .mypy_cache .cache build/ dist/ *.egg-info 2>/dev/null || true
endif
	@echo "${GREEN}Очистка завершена${NC}"

mini-reset: ## Пересборка контейнеров
	@echo "${RED}Пересоздание проекта${NC}"
	docker-compose down
	docker-compose build
	docker-compose up -d
	@echo "${YELLOW}Жду запуска сервисов...${NC}"
	sleep 5
	alembic upgrade head
	@echo "${GREEN}Проект собран${NC}"

reset: ## Полный сброс (остановить, удалить volumes, пересобрать)
	@echo "${RED}ВНИМАНИЕ: Полный сброс проекта${NC}"
	@echo "Это удалит все данные в БД!"
	docker-compose down -v
	docker-compose build --no-cache
	docker-compose up -d
	sleep 5
	alembic upgrade head
	@echo "${GREEN}Проект сброшен и перезапущен${NC}"
