@echo off
REM Automatyczna instalacja SVG Browser (Windows)

echo 🎨 SVG Browser - Automatyczna instalacja
echo =========================================

REM Sprawdź Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python nie jest zainstalowany lub nie jest w PATH
    echo 💡 Zainstaluj Python z https://python.org
    pause
    exit /b 1
)

echo ✅ Python dostępny

REM Sprawdź wersję Pythona
python -c "import sys; exit(0 if sys.version_info >= (3, 8, 1) else 1)" >nul 2>&1
if errorlevel 1 (
    echo ❌ Wymagany Python 3.8.1+
    pause
    exit /b 1
)

REM Sprawdź Poetry
poetry --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Poetry nie znalezione - użyje pip
    set INSTALL_METHOD=pip
) else (
    echo ✅ Poetry dostępne
    set INSTALL_METHOD=poetry
)

REM Instalacja
if "%INSTALL_METHOD%"=="poetry" (
    echo 📦 Instalacja przez Poetry...
    
    REM Napraw pyproject.toml jeśli potrzeba
    findstr "python = \"^3.8\"" pyproject.toml >nul 2>&1
    if not errorlevel 1 (
        echo 🔧 Naprawiam wymagania Pythona...
        powershell -Command "(Get-Content pyproject.toml) -replace 'python = \"\^3.8\"', 'python = \"^3.8.1\"' | Set-Content pyproject.toml"
    )
    
    REM Wyczyść cache i zainstaluj
    poetry cache clear --all pypi 2>nul
    poetry env remove python 2>nul
    poetry install
    
    if errorlevel 1 (
        echo ❌ Błąd instalacji Poetry
        pause
        exit /b 1
    )
    
    echo ✅ Instalacja Poetry zakończona
    
) else (
    echo 📦 Instalacja przez pip...
    python -m pip install -r requirements.txt
    python -m pip install -e .
    
    if errorlevel 1 (
        echo ❌ Błąd instalacji pip
        pause
        exit /b 1
    )
    
    echo ✅ Instalacja pip zakończona
)

REM Konfiguracja
if not exist .env (
    if exist .env.example (
        echo 📋 Kopiowanie .env.example -^> .env
        copy .env.example .env >nul
    ) else (
        echo 📋 Tworzenie podstawowego .env
        echo SCAN_PATHS=./test-svgs > .env
        echo PORT=5000 >> .env
        echo DEBUG=True >> .env
    )
)

REM Pliki testowe
if not exist test-svgs (
    echo 🧪 Tworzenie plików testowych...
    python create_test_structure.py 2>nul || (
        mkdir test-svgs\graphics 2>nul
        echo ^<?xml version="1.0"?^> > test-svgs\graphics\test.svg
        echo ^<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"^> >> test-svgs\graphics\test.svg
        echo   ^<circle cx="50" cy="50" r="40" fill="#3498db"/^> >> test-svgs\graphics\test.svg
        echo   ^<text x="50" y="55" text-anchor="middle" fill="white"^>SVG^</text^> >> test-svgs\graphics\test.svg
        echo ^</svg^> >> test-svgs\graphics\test.svg
        echo ✅ Utworzono podstawowy plik testowy
    )
)

echo.
echo 🎉 Instalacja zakończona!
echo.
echo 🚀 Uruchomienie:

if "%INSTALL_METHOD%"=="poetry" (
    echo    poetry run python svg_browser/app.py
) else (
    echo    python svg_browser/app.py
)

echo    lub: python start.py
echo.
echo 🌐 Serwer będzie dostępny na: http://localhost:5000

pause
