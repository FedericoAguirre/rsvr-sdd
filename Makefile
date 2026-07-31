SHELL := /bin/bash
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

.PHONY: help
help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Database targets:"
	@echo "  db-up      Start PostgreSQL in Docker"
	@echo "  db-stop    Stop PostgreSQL"
	@echo "  db-logs    Tail database logs"
	@echo "  db-prune   Stop DB and prune Docker resources"
	@echo ""
	@echo "Local development targets:"
	@echo "  serve      Run Django dev server locally (http://localhost:8000)"
	@echo "  migrate    Run database migrations"
	@echo "  seed       Seed demo data (classes, equipment, clients)"
	@echo "  createsuperuser  Create admin account"
	@echo "  test       Run pytest suite"
	@echo "  lint       Run ruff linter on backend/"
	@echo "  format     Format code with ruff"
	@echo ""
	@echo "Pre-deployment testing:"
	@echo "  docker-build   Build web Docker image (for production testing)"
	@echo "  docker-up      Start full stack in Docker (DB + web container)"
	@echo "  docker-down    Stop full Docker stack"
	@echo "  install        Install Python dependencies with uv"

.PHONY: db-up
db-up:
	docker-compose up -d db

.PHONY: db-stop
db-stop:
	docker-compose stop db

.PHONY: db-logs
db-logs:
	docker compose logs -f db

.PHONY: db-prune
db-prune: db-stop
	docker container prune -f
	docker image prune -f
	docker volume prune -f

.PHONY: serve
serve:
	cd backend && uv run manage.py runserver

.PHONY: migrate
migrate:
	cd backend && uv run manage.py migrate

.PHONY: seed
seed:
	cd backend && uv run manage.py seed_data

.PHONY: createsuperuser
createsuperuser:
	cd backend && uv run manage.py createsuperuser

.PHONY: test
test:
	cd backend && uv run pytest

.PHONY: lint
lint:
	cd backend && uv run ruff check .

.PHONY: format
format:
	cd backend && uv run ruff format .

# Pre-deployment: test in actual Docker container before pushing to production
.PHONY: docker-build
docker-build:
	docker build -f backend/Dockerfile -t rsvr-sdd:latest backend/

.PHONY: docker-up
docker-up:
	docker-compose -f docker-compose.prod.yml up -d

.PHONY: docker-down
docker-down:
	docker-compose -f docker-compose.prod.yml down

.PHONY: install
install:
	cd backend && uv sync
