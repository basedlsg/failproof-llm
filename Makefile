# Makefile for failproof-llm

.PHONY: setup lint test demo dev

# ==============================================================================
# SETUP
# ==============================================================================

setup: setup-backend setup-frontend

setup-backend:
	@echo "Installing backend dependencies..."
	pip install -r requirements.txt

setup-frontend:
	@echo "Installing frontend dependencies..."
	cd web && npm install

# ==============================================================================
# LINTING
# ==============================================================================

lint: lint-backend lint-frontend

lint-backend:
	@echo "Linting backend..."
	pip install ruff
	ruff check backend

lint-frontend:
	@echo "Linting frontend..."
	cd web && npm run lint


# ==============================================================================
type-check-backend:
	@echo "Type checking backend..."
	mypy backend

type-check-frontend:
	@echo "Type checking frontend..."
	cd web && npm run type-check

test-backend-cov:
validate-schemas:
	@echo "Validating JSONL schemas..."
	python scripts/validate_schemas.py
	@echo "Running backend tests with coverage..."
	pytest --cov=backend --cov-report=xml --cov-fail-under=80
# TESTING
# ==============================================================================

test: test-backend test-frontend

test-backend:
	@echo "Running backend tests..."
	pytest

test-frontend:
	@echo "Running frontend tests..."
	cd web && npm run test


# ==============================================================================
# DEMO
# ==============================================================================

demo:
	@echo "Running demo..."
	@RUN_ID=$$(python -m backend.cli run-suite --suite-path suites/json_api/smoke_test.jsonl | tail -n 1 | awk '{print $$NF}') && \
	echo "Using RUN_ID: $$RUN_ID" && \
	python -m backend.cli classify-run --run-id $$RUN_ID && \
	python -m backend.cli score-run --run-id $$RUN_ID && \
	python -m backend.cli export-report --run-id $$RUN_ID && \
	echo "Demo complete. RUN_ID: $$RUN_ID. Report at reports/$$RUN_ID.md"


# ==============================================================================
# DEVELOPMENT
# ==============================================================================

dev:
	@echo "Starting backend and frontend servers..."
	@echo "Backend running on http://127.0.0.1:8000"
	@echo "Frontend development server will be available shortly."
	uvicorn backend.api.main:app --reload & \
	(cd web && npm run dev)
