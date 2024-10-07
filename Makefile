# Variables
POETRY := poetry

.PHONY: help install test lint format check-types pre-commit run-queue

# Show help
help:
	@echo "Makefile commands:"
	@echo "  install         Install project dependencies"
	@echo "  test            Run tests"
	@echo "  lint            Run flake8 for linting"
	@echo "  format          Run black for code formatting"
	@echo "  check-types     Run mypy for type checking"
	@echo "  pre-commit      Run all pre-commit hooks"
	@echo "  run-queue       Run the QueueTeePie task queue"
	@echo "  clean           Remove build, test, coverage, and Python artifacts"

# Install dependencies using Poetry
install:
	@$(POETRY) install

# Run tests
pytest:
	@$(POETRY) run pytest

unittest:
	@$(POETRY) run python -m unittest discover

# Run flake8 for linting
lint:
	@$(POETRY) run flake8 queue_tee_pie tests

# Run black for code formatting
format:
	@$(POETRY) run black queue_tee_pie tests

# Run mypy for type checking
check-types:
	@$(POETRY) run mypy queue_tee_pie

# Run pre-commit hooks
pre-commit:
	@$(POETRY) run pre-commit run --all-files

# Run the QueueTeePie task queue
run-queue:
	@$(POETRY) run python -m queue_tee_pie.core

# Clean up Python and build artifacts
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	rm -rf .mypy_cache/
	rm -rf .pytest_cache/
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
