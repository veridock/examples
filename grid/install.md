# 📦 Instrukcja instalacji SVG Browser

## Szybka instalacja

### 1️⃣ Automatyczna instalacja (zalecana)

```bash
# Sklonuj lub pobierz projekt
git clone <repository_url> svg_browser
cd svg_browser

# Uruchom automatyczny starter
python start.py
```

Skrypt automatycznie:
- ✅ Sprawdzi wymagania systemowe
- ✅ Zainstaluje zależności  
- ✅ Skonfiguruje pliki
- ✅ Stworzy pliki testowe (opcjonalnie)
- ✅ Uruchomi serwer

### 2️⃣ Ręczna instalacja

#### Wymagania
- **Python 3.8+**
- **Poetry** (zalecane) lub **pip**

#### Kroki instalacji

```bash
# 1. Przejdź do katalogu projektu
cd svg_browser

# 2a. Instalacja przez Poetry (zalecane)
poetry install

# 2b. Alternatywnie przez pip
pip install -r requirements.txt
pip install -e .

# 3. Konfiguracja
cp .env.example .env
# Edytuj .env i ustaw ścieżki SCAN_PATHS

# 4. Stwórz pliki testowe (opcjonalnie)
python create_test_structure.py

# 5. Uruchomienie
poetry run python svg_browser/app.py
# lub: python svg_browser/app.py
```

## Szczegółowe opcje instalacji

### Poetry (zalecane)

```bash
# Instalacja Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Instalacja projektu
poetry install

# Uruchomienie
poetry run svg_browser
# lub
poetry shell
python svg_browser/app.py
```

### Pip + virtualenv

```bash
# Stworzenie środowiska wirtualnego
python -m venv venv

# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instalacja
pip install -r requirements.txt
pip install -e .

# Uruchomienie
python svg_browser/app.py
```

### Docker

```bash
# Budowanie obrazu
docker build -t svg_browser .

# Uruchomienie (montuj katalogi z SVG)
docker run -p 5000:5000 \
  -v /path/to/your/svg:/mnt/svg:ro \
  -e SCAN_PATHS=/mnt/svg \
  svg_browser

# Lub przez docker-compose
docker-compose up
```

## Konfiguracja

### Plik .env

```bash
# Ścieżki do skanowania (WYMAGANE)
SCAN_PATHS=/path/to/svg1,/path/to/svg2

# Opcjonalne
PORT=5000
DEBUG=False
```

### Przykłady ścieżek

**Windows:**
```bash
SCAN_PATHS=C:\Users\Username\Pictures\SVG,C:\Projects\icons
```

**Linux/Mac:**
```bash
SCAN_PATHS=/home/username/svg-files,/usr/local/share/icons
```

**Ścieżki względne:**
```bash
SCAN_PATHS=./test-svgs,../svg-assets
```

## Testowanie instalacji

### Pliki testowe

```bash
# Automatyczne tworzenie
python create_test_structure.py

# Ręczne ustawienie
mkdir -p test-svgs/{graphics,pwa,metadata}
echo 'SCAN_PATHS=./test-svgs' > .env
```

### Sprawdzenie działania

```bash
# Uruchomienie serwera
python svg_browser/app.py

# Otwórz przeglądarkę:
# http://localhost:5000
```

## Rozwiązywanie problemów

### Błędy instalacji

**Problem**: `ModuleNotFoundError`
```bash
# Rozwiązanie - sprawdź instalację
pip list | grep -E "(flask|lxml|python-dotenv)"
poetry show
```

**Problem**: `lxml` nie może się zainstalować
```bash
# Linux (Ubuntu/Debian)
sudo apt-get install libxml2-dev libxslt-dev
pip install lxml

# macOS
brew install libxml2 libxslt
pip install lxml

# Windows - użyj pre-compiled wheel
pip install --only-binary=lxml lxml
```

### Problemy z konfiguracją

**Problem**: Brak pliku .env
```bash
# Rozwiązanie
cp .env.example .env
# Edytuj .env i ustaw ścieżki
```

**Problem**: Ścieżki nie istnieją
```bash
# Sprawdź ścieżki
ls -la /path/to/your/svg/files

# Lub stwórz testowe
python create_test_structure.py
```

### Problemy z uruchomieniem

**Problem**: Port zajęty
```bash
# Zmień port w .env
PORT=5001
```

**Problem**: Brak uprawnień do ścieżek
```bash
# Sprawdź uprawnienia
ls -la /path/to/svg/

# Linux/Mac - dodaj uprawnienia
chmod +r /path/to/svg/files
```

## Makefile (Linux/Mac)

```bash
# Wszystkie komendy przez make
make help          # Pomoc
make install       # Instalacja
make run           # Uruchomienie
make dev           # Tryb debug
make test          # Testy
make clean         # Czyszczenie
```

## Deinstalacja

### Poetry
```bash
poetry env remove python
rm -rf .venv/
```

### Pip
```bash
pip uninstall svg_browser
deactivate  # jeśli używasz venv
rm -rf venv/
```

### Pliki projektu
```bash
rm -rf svg_browser/
```

## Wsparcie

Jeśli masz problemy z instalacją:

1. ✅ Sprawdź wymagania systemowe (Python 3.8+)
2. ✅ Upewnij się że plik .env istnieje i ma poprawne ścieżki
3. ✅ Użyj `python start.py` dla automatycznej diagnozy
4. ✅ Sprawdź logi błędów podczas uruchomienia

**Automatyczna diagnoza:**
```bash
python start.py  # Sprawdzi wszystkie wymagania
```