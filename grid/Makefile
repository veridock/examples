# Makefile dla SVG Browser

.PHONY: help install run dev clean test format lint docker-build docker-run

# Domyślny cel
help:
	@echo "🎨 SVG Browser - Dostępne komendy:"
	@echo ""
	@echo "  install     - Instalacja zależności przez Poetry"
	@echo "  install-pip - Instalacja zależności przez pip"
	@echo "  run         - Uruchomienie serwera (produkcja)"
	@echo "  dev         - Uruchomienie serwera (tryb debug)"
	@echo "  test        - Uruchomienie testów"
	@echo "  format      - Formatowanie kodu (black)"
	@echo "  lint        - Sprawdzenie kodu (flake8)"
	@echo "  clean       - Czyszczenie plików tymczasowych"
	@echo "  docker-build- Budowanie obrazu Docker"
	@echo "  docker-run  - Uruchomienie w kontenerze"
	@echo "  package     - Tworzenie pakietu dystrybucyjnego"
	@echo ""

# Instalacja przez Poetry
install:
	@echo "📦 Instalowanie zależności przez Poetry..."
	poetry install

# Instalacja przez pip
install-pip:
	@echo "📦 Instalowanie zależności przez pip..."
	pip install -r requirements.txt
	pip install -e .

# Uruchomienie serwera (produkcja)
run:
	@echo "🚀 Uruchamianie SVG Browser (produkcja)..."
	poetry run python svg_browser/app.py

# Uruchomienie serwera (tryb debug)
dev:
	@echo "🔧 Uruchamianie SVG Browser (tryb debug)..."
	@echo "DEBUG=True" > .env.local
	@cat .env >> .env.local 2>/dev/null || true
	DEBUG=True poetry run python svg_browser/app.py

# Uruchomienie przez pip
run-pip:
	@echo "🚀 Uruchamianie SVG Browser przez pip..."
	python svg_browser/app.py

# Tworzenie testowych plików SVG
create-test-files:
	@echo "📁 Tworzenie testowych plików SVG..."
	mkdir -p test-svgs/graphics test-svgs/pwa test-svgs/metadata
	@echo "Testowe pliki zostaną stworzone w katalogu test-svgs/"

# Formatowanie kodu
format:
	@echo "✨ Formatowanie kodu..."
	poetry run black svg_browser/
	poetry run black *.py

# Sprawdzenie kodu
lint:
	@echo "🔍 Sprawdzanie kodu..."
	poetry run flake8 svg_browser/ --max-line-length=88 --extend-ignore=E203

# Testy
test:
	@echo "🧪 Uruchamianie testów..."
	poetry run pytest tests/ -v --cov=svg_browser

# Czyszczenie
clean:
	@echo "🧹 Czyszczenie plików tymczasowych..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/
	rm -f .env.local

# Docker
docker-build:
	@echo "🐳 Budowanie obrazu Docker..."
	docker build -t svg_browser .

docker-run:
	@echo "🐳 Uruchamianie w kontenerze..."
	docker run -p 5000:5000 -v $(PWD)/.env:/app/.env svg_browser

# Tworzenie pakietu
package:
	@echo "📦 Tworzenie pakietu dystrybucyjnego..."
	poetry build

# Instalacja z pakietu
install-local:
	@echo "📦 Instalacja z lokalnego pakietu..."
	pip install dist/*.whl

# Sprawdzenie środowiska
check-env:
	@echo "🔍 Sprawdzanie środowiska..."
	@if [ ! -f .env ]; then echo "❌ Brak pliku .env - skopiuj .env.example"; exit 1; fi
	@echo "✅ Plik .env istnieje"
	@python -c "import sys; print(f'Python: {sys.version}')"
	@poetry --version 2>/dev/null || echo "Poetry: nie zainstalowane"

# Pełna instalacja i uruchomienie
setup: check-env install create-test-files
	@echo "✅ Projekt gotowy do użycia!"
	@echo "Uruchom: make run"

# Pomoc rozszerzona
info:
	@echo "🎨 SVG Browser - Informacje o projekcie"
	@echo ""
	@echo "📁 Struktura projektu:"
	@echo "  svg_browser/        - Kod źródłowy"
	@echo "  svg_browser/app.py  - Główny serwer"
	@echo "  templates/          - Szablony HTML"
	@echo "  .env                - Konfiguracja (skopiuj z .env.example)"
	@echo ""
	@echo "🚀 Szybki start:"
	@echo "  1. make install"
	@echo "  2. cp .env.example .env"
	@echo "  3. # Edytuj .env i ustaw ścieżki SCAN_PATHS"
	@echo "  4. make run"
	@echo ""
	@echo "🌐 Serwer będzie dostępny na: http://localhost:5000"