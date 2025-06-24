.PHONY: help install test test-watch lint format clean build serve deploy push

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

# Push changes to remote repository with auto-generated message
push:
	@echo "🚀 Preparing to push changes..."
	git add .
	@if git diff --cached --quiet; then \
		echo "No changes to commit"; \
		exit 0; \
	fi
	@echo "🚀 Changes to be committed:"
	@git status -s
	@echo ""
	@echo "📦 Auto-generating commit message..."
	@echo ""
	@if git diff --cached --name-status | grep -q '^[A|M]\s.*\.pwa\.svg'; then \
		echo "🔧 Updated SVG PWA applications:"; \
		git diff --cached --name-status | grep '\.pwa\.svg' | sed 's/^[A-Z]\s*/  • /'; \
	fi
	@if git diff --cached --name-status | grep -q '^[A|M]\s.*\.js'; then \
		echo "🛠️  Updated JavaScript files:"; \
		git diff --cached --name-status | grep '\.js' | sed 's/^[A-Z]\s*/  • /'; \
	fi
	@if git diff --cached --name-status | grep -q '^[A|M]\s.*\.md'; then \
		echo "📄 Updated documentation:"; \
		git diff --cached --name-status | grep '\.md' | sed 's/^[A-Z]\s*/  • /'; \
	fi
	@echo ""
	@read -p "📝 Press Enter to continue with auto-generated message or type a custom message: " custom_msg; \
	if [ -z "$$custom_msg" ]; then \
		git commit -m "🔧 Update project files" -m "$(shell git diff --cached --name-status | sed 's/^/• /' | head -5)" && \
		git push; \
	else \
		git commit -m "$$custom_msg" && git push; \
	fi

# Run all tests before committing
pre-commit: test lint

# Default target
.DEFAULT_GOAL := help
