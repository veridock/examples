# 🛠️ Rozwiązywanie problemów SVG Browser

## Błąd: "The current project's supported Python range..."

**Problem:** Poetry nie może zainstalować zależności z powodu konfliktu wersji Pythona.

```
The current project's supported Python range (>=3.8,<4.0) is not compatible with some of the required packages Python requirement:
- flake8 requires Python >=3.8.1
```

### ✅ Rozwiązania:

#### 1. Automatyczna naprawa (zalecane)
```bash
python fix_install.py
# lub
make fix
```

#### 2. Ręczna naprawa Poetry
```bash
# Wyczyść cache
poetry cache clear --all pypi

# Usuń środowisko
poetry env remove python

# Zainstaluj ponownie
poetry install
```

#### 3. Alternatywna instalacja przez pip
```bash
python quick_start.py
# lub
pip install -r requirements.txt
pip install -e .
```

## Błąd: "ModuleNotFoundError"

**Problem:** Brak wymaganych modułów Python.

### ✅ Rozwiązania:

#### Sprawdź instalację
```bash
python diagnose.py  # Pełna diagnostyka
```

#### Zainstaluj brakujące moduły
```bash
# Poetry
poetry install

# Pip
pip install flask python-dotenv lxml
```

#### Problem z lxml
```bash
# Ubuntu/Debian
sudo apt-get install libxml2-dev libxslt-dev python3-dev
pip install lxml

# CentOS/RHEL
sudo yum install libxml2-devel libxslt-devel python3-devel
pip install lxml

# macOS
brew install libxml2 libxslt
pip install lxml

# Windows
pip install --only-binary=lxml lxml
```

## Błąd: "Brak pliku .env"

**Problem:** Serwer nie może znaleźć konfiguracji.

### ✅ Rozwiązania:

```bash
# Skopiuj przykład
cp .env.example .env

# Lub stwórz ręcznie
cat > .env << EOF
SCAN_PATHS=./test-svgs,/path/to/your/svg/files
PORT=5000
DEBUG=True
EOF
```

## Błąd: "Brak skonfigurowanych ścieżek"

**Problem:** Plik .env nie ma SCAN_PATHS lub ścieżki nie istnieją.

### ✅ Rozwiązania:

#### Sprawdź konfigurację
```bash
cat .env  # Pokaż zawartość

# Dodaj ścieżki
echo "SCAN_PATHS=/path/to/svg/files" >> .env
```

#### Stwórz pliki testowe
```bash
python create_test_structure.py

# Lub ręcznie
mkdir -p test-svgs/graphics
echo 'SCAN_PATHS=./test-svgs' > .env
```

#### Sprawdź ścieżki
```bash
# Linux/Mac
ls -la /path/to/svg/files

# Windows
dir "C:\path\to\svg\files"
```

## Błąd: "Port already in use"

**Problem:** Port 5000 jest zajęty przez inną aplikację.

### ✅ Rozwiązania:

#### Zmień port
```bash
# W pliku .env
PORT=5001

# Lub przez zmienną środowiskową
PORT=5001 python svg_browser/app.py
```

#### Sprawdź co używa portu
```bash
# Linux/Mac
lsof -i :5000
netstat -tulpn | grep 5000

# Windows
netstat -ano | findstr 5000
```

## Problemy z uruchomieniem

### "Permission denied"

```bash
# Linux/Mac - sprawdź uprawnienia
chmod +x install.sh
chmod +r /path/to/svg/files

# Sprawdź czy katalogi istnieją
ls -la /path/to/svg/
```

### "Python not found"

```bash
# Sprawdź Python
which python3
python3 --version

# Dodaj do PATH (Linux/Mac)
export PATH="/usr/bin/python3:$PATH"

# Windows - zainstaluj Python z python.org
```

## Problemy z Docker

### "docker: command not found"

```bash
# Zainstaluj Docker
# Linux (Ubuntu)
sudo apt-get install docker.io

# macOS
brew install docker

# Windows - Docker Desktop
```

### "Permission denied" (Docker)

```bash
# Linux - dodaj użytkownika do grupy docker
sudo usermod -aG docker $USER
logout  # Zaloguj się ponownie
```

### Problemy z montowaniem katalogów

```yaml
# W docker-compose.yml - popraw ścieżki
volumes:
  - "/absolute/path/to/svg:/mnt/svg:ro"
  
# Windows
volumes:
  - "C:/Users/Username/SVG:/mnt/svg:ro"
```

## Problemy specyficzne dla systemu

### Windows

#### "python nie jest rozpoznane"
```cmd
# Zainstaluj Python z python.org
# Upewnij się że "Add Python to PATH" jest zaznaczone

# Sprawdź PATH
echo %PATH%
```

#### Problemy z Poetry
```cmd
# Zainstaluj Poetry
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# Lub pip
pip install poetry
```

### macOS

#### Problemy z lxml
```bash
# Zainstaluj przez Homebrew
brew install libxml2 libxslt
export LDFLAGS="-L$(brew --prefix libxml2)/lib"
export CPPFLAGS="-I$(brew --prefix libxml2)/include"
pip install lxml
```

### Linux

#### Brak uprawnień
```bash
# Dodaj uprawnienia do katalogu
sudo chown -R $USER:$USER /path/to/svg/files
chmod -R 755 /path/to/svg/files
```

## Narzędzia diagnostyczne

### Pełna diagnostyka
```bash
python diagnose.py
```

### Sprawdzenie środowiska
```bash
python start.py  # Interaktywne sprawdzenie
```

### Logs serwera
```bash
# Uruchom z debug
DEBUG=True python svg_browser/app.py

# Sprawdź logi
tail -f /var/log/svg_browser.log
```

## Częste pytania

### Q: Czy działa na Python 3.7?
A: Nie, wymagany jest Python 3.8.1+ z powodu zależności.

### Q: Czy mogę skanować katalogi systemowe?
A: Tak, ale upewnij się że masz uprawnienia do odczytu.

### Q: Czy SVG z JavaScript są bezpieczne?
A: Przeglądarka wyświetla je w kontrolowanym środowisku, ale zachowaj ostrożność z nieznanymi plikami.

### Q: Jak dodać więcej ścieżek do skanowania?
A: Edytuj .env i dodaj ścieżki oddzielone przecinkami:
```bash
SCAN_PATHS=/path1,/path2,/path3
```

## Gdzie szukać pomocy

1. **Sprawdź logi błędów** podczas uruchomienia
2. **Uruchom diagnostykę:** `python diagnose.py`
3. **Sprawdź pliki:** Czy wszystkie wymagane pliki istnieją?
4. **Sprawdź uprawnienia:** Czy możesz odczytać katalogi SVG?
5. **Sprawdź wersję Pythona:** `python --version`

## Rozwiązania awaryjne

### Kompletny reset