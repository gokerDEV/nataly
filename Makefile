.PHONY: help install install-dev test test-cov lint format clean build publish

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install the package in development mode
	pip install -e .

install-dev:  ## Install the package with development dependencies
	pip install -e ".[dev]"

test:  ## Run tests
	pytest tests/ -v

test-cov:  ## Run tests with coverage
	pytest tests/ -v --cov=nataly --cov-report=html --cov-report=term-missing

lint:  ## Run linting
	flake8 nataly/ tests/
	mypy nataly/

format:  ## Format code with black
	black nataly/ tests/

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build:  ## Build the package
	python setup.py sdist bdist_wheel

publish:  ## Publish to PyPI (requires twine)
	twine upload dist/*

check:  ## Check package for common issues
	python setup.py check
	twine check dist/*

docs:  ## Build documentation (if using Sphinx)
	cd docs && make html

all: clean install-dev format lint test  ## Run all checks: clean, install, format, lint, test 