.PHONY: help install test test-watch lint format clean build serve deploy

# Project information
PROJECT_NAME := veridock
VERSION := 1.0.0
PORT := 8000

# Directories
SRC_DIR := examples
TEST_DIR := tests
DIST_DIR := dist
NODE_MODULES := node_modules

# Commands
PYTHON := python3
NPM := npm
NODE := node
SERVE := $(PYTHON) -m http.server $(PORT)

# Default target
help:
	@echo "\n🚀 $(PROJECT_NAME) v$(VERSION) - Available targets:\n"
	@echo "  make install      Install project dependencies"
	@echo "  make test         Run all tests"
	@echo "  make test-watch   Run tests in watch mode"
	@echo "  make lint         Lint source files"
	@echo "  make format       Format source files"
	@echo "  make clean        Clean build artifacts"
	@echo "  make build        Build project"
	@echo "  make serve        Start development server"
	@echo "  make deploy       Deploy project"

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	$(NPM) install

# Run tests
test:
	@echo "🧪 Running tests..."
	@for dir in $(shell find $(SRC_DIR) -type d -name "test" -o -name "tests"); do \
		echo "\n📁 Testing in $$dir"; \
		(cd $$dir/.. && $(NPM) test || exit 1); \
	done

# Run tests in watch mode
test-watch:
	@echo "👀 Starting test watcher..."
	$(NPM) test -- --watchAll

# Lint source files
lint:
	@echo "🔍 Linting source files..."
	$(NPM) run lint

# Format source files
format:
	@echo "✨ Formatting source files..."
	$(NPM) run format

# Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf $(DIST_DIR)
	rm -rf $(NODE_MODULES)
	find . -name "*.log" -delete

# Build project
build: clean
	@echo "🔨 Building project..."
	@mkdir -p $(DIST_DIR)
	@cp -r $(SRC_DIR) $(DIST_DIR)/
	@echo "✅ Build complete!"

# Start development server
serve:
	@echo "🌐 Starting development server at http://localhost:$(PORT)"
	@echo "📂 Serving from: $(shell pwd)/$(SRC_DIR)"
	@echo "🛑 Press Ctrl+C to stop"
	@cd $(SRC_DIR) && $(SERVE)

# Deploy project
deploy: test build
	@echo "🚀 Deploying project..."
	@if [ -z "$(GIT_REMOTE)" ]; then \
		echo "❌ GIT_REMOTE is not set. Please set it with: make deploy GIT_REMOTE=your-remote"; \
		exit 1; \
	fi
	@echo "📦 Pushing to $(GIT_REMOTE) $(shell git rev-parse --abbrev-ref HEAD)"
	git push $(GIT_REMOTE) $(shell git rev-parse --abbrev-ref HEAD)
	@echo "✅ Deployment complete!"

# Run all tests before committing
pre-commit: test lint

# Default target
.DEFAULT_GOAL := help
