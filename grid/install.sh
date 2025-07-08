#!/bin/bash
# Automatyczna instalacja SVG Browser (Linux/Mac)

set -e

echo "🎨 SVG Browser - Automatyczna instalacja"
echo "========================================="

# Sprawdź Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 nie jest zainstalowany"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python $PYTHON_VERSION"

# Sprawdź czy mamy odpowiednią wersję
python3 -c 'import sys; exit(0 if sys.version_info >= (3, 8, 1) else 1)' || {
    echo "❌ Wymagany Python 3.8.1+"
    exit 1
}

# Sprawdź Poetry
if command -v poetry &> /dev/null; then
    echo "✅ Poetry dostępne"
    INSTALL_METHOD="poetry"
else
    echo "⚠️  Poetry nie znalezione - użyje pip"
    INSTALL_METHOD="pip"
fi

# Instalacja
if [ "$INSTALL_METHOD" = "poetry" ]; then
    echo "📦 Instalacja przez Poetry..."
    
    # Napraw pyproject.toml jeśli potrzeba
    if grep -q 'python = "\^3.8"' pyproject.toml 2>/dev/null; then
        echo "🔧 Naprawiam wymagania Pythona..."
        sed -i.bak 's/python = "\^3.8"/python = "^3.8.1"/' pyproject.toml
    fi
    
    # Wyczyść cache i zainstaluj
    poetry cache clear --all pypi 2>/dev/null || true
    poetry env remove python 2>/dev/null || true
    poetry install
    
    echo "✅ Instalacja Poetry zakończona"
    
else
    echo "📦 Instalacja przez pip..."
    python3 -m pip install -r requirements.txt
    python3 -m pip install -e .
    
    echo "✅ Instalacja pip zakończona"
fi

# Konfiguracja
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        echo "📋 Kopiowanie .env.example -> .env"
        cp .env.example .env
    else
        echo "📋 Tworzenie podstawowego .env"
        cat > .env << EOF
SCAN_PATHS=./test-svgs
PORT=5000
DEBUG=True
EOF
    fi
fi

# Pliki testowe
if [ ! -d test-svgs ]; then
    echo "🧪 Tworzenie plików testowych..."
    python3 create_test_structure.py 2>/dev/null || {
        mkdir -p test-svgs/graphics
        cat > test-svgs/graphics/test.svg << 'EOF'
<?xml version="1.0"?>
<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="40" fill="#3498db"/>
  <text x="50" y="55" text-anchor="middle" fill="white">SVG</text>
</svg>
EOF
        echo "✅ Utworzono podstawowy plik testowy"
    }
fi

echo ""
echo "🎉 Instalacja zakończona!"
echo ""
echo "🚀 Uruchomienie:"

if [ "$INSTALL_METHOD" = "poetry" ]; then
    echo "   poetry run python svg_browser/app.py"
else
    echo "   python3 svg_browser/app.py"
fi

echo "   lub: python3 start.py"
echo ""
echo "🌐 Serwer będzie dostępny na: http://localhost:5000"
