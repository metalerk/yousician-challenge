# Variables
APP_NAME = yousician_api
IMAGE_NAME = yousician_api
PORT = 8000

# Environment
ENV_FILE = .env

# Default target
.DEFAULT_GOAL := help

## Run FastAPI application locally
run:
	@echo "🚀 Running FastAPI application..."
	uvicorn app.main:app --reload --host 0.0.0.0 --port $(PORT)

## Install dependencies
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt

## Lint code with flake8
lint:
	@echo "🧹 Running linter..."
	flake8 app --exclude __init__.py

## Test the application with pytest
test:
	@echo "🧪 Running tests..."
	pytest tests

## Format code using Black
format:
	@echo "✨ Formatting code with Black..."
	black app

## Display help
help:
	@echo "🛠️  Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
