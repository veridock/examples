# SVG Browser 🎨

Lokalny serwer do przeglądania i kategoryzacji plików SVG z automatycznym wykrywaniem PWA i metadanych.

## Funkcje

- **Rekursywne skanowanie** wybranych ścieżek w poszukiwaniu plików SVG
- **Automatyczna kategoryzacja** na 3 grupy:
  - 📊 **Graficzne** - zwykłe pliki SVG
  - ⚙️ **PWA/JS** - pliki SVG z kodem JavaScript (interaktywne aplikacje)
  - 📋 **Metadane** - pliki SVG z metadanymi (tytuł, opis, autor, itp.)
- **Grid preview** - miniaturki wszystkich plików z podglądem
- **Responsywny interfejs** z tabami do przełączania kategorii
- **Informacje o plikach** - ścieżka, rozmiar, metadane
- **Konfiguracja przez .env** - łatwe zarządzanie ścieżkami do skanowania

## Instalacja

### Wymagania
- Python 3.8.1+
- Poetry (do zarządzania zależnościami) lub pip

### Automatyczna instalacja

#### Linux/Mac:
```bash
./install.sh
```

#### Windows:
```cmd
install.bat
```

#### Uniwersalna (Python):
```bash
python quick_start.py    # Instalacja + uruchomienie
python start.py          # Interaktywny starter
```

### Kroki instalacji

1. **Zainstaluj Poetry** (jeśli nie masz):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. **Sklonuj lub stwórz projekt**:
```bash
mkdir svg_browser
cd svg_browser
```

3. **Skopiuj pliki projektu** do katalogu

4. **Zainstaluj zależności**:
```bash
poetry install
```

5. **Skonfiguruj ścieżki w .env**:
```bash
cp .env.example .env
# Edytuj plik .env i ustaw swoje ścieżki
```

## Konfiguracja

Edytuj plik `.env` i ustaw ścieżki do skanowania:

```bash
# Przykład dla Windows
SCAN_PATHS=C:\Users\Username\Documents\SVG,C:\Projects\icons

# Przykład dla Linux/Mac
SCAN_PATHS=/home/username/svg-files,/usr/local/share/icons,~/Pictures/SVG

# Opcjonalne ustawienia
PORT=5000
DEBUG=False
```

## Uruchomienie

### Przez Poetry:
```bash
poetry run python -m svg_browser.app
```

### Lub przez skrypt:
```bash
poetry run svg_browser
```

### Bezpośrednio przez Python:
```bash
poetry shell
python svg_browser/app.py
```

### Szybki start (bez Poetry):
```bash
python quick_start.py
```

### Automatyczny starter:
```bash
python start.py
```

Serwer będzie dostępny na: **http://localhost:5000**

## Użytkowanie

1. **Otwórz przeglądarkę** i przejdź do http://localhost:5000
2. **Kliknij "Skanuj pliki SVG"** aby rozpocząć skanowanie
3. **Przełączaj między tabami** aby przeglądać różne kategorie:
   - **Graficzne** - zwykłe pliki SVG bez JavaScript i metadanych
   - **PWA/JS** - interaktywne pliki SVG z kodem JavaScript
   - **Metadane** - pliki SVG z tytułem, opisem lub innymi metadanymi
4. **Kliknij na plik** aby otworzyć go w nowej karcie

## Jak działa kategoryzacja

### PWA/JS (Aplikacje z JavaScript)
Pliki są klasyfikowane jako PWA/JS jeśli zawierają:
- Tag `<script>`
- Atrybuty event handlery (onclick, onload, onmouseover)
- Linki `javascript:`

### Metadane
Pliki są klasyfikowane jako zawierające metadane jeśli mają:
- Tag `<title>` z tekstem
- Tag `<desc>` z opisem
- Atrybuty `data-*` (data-name, data-author, etc.)
- Element `<metadata>`

### Graficzne
Wszystkie pozostałe pliki SVG bez JavaScript i metadanych.

## Struktura projektu

```
svg_browser/
├── pyproject.toml          # Konfiguracja Poetry
├── .env                    # Zmienne środowiskowe
├── README.md              # Ten plik
└── svg_browser/
    ├── __init__.py        # Inicjalizacja pakietu
    ├── app.py            # Główny serwer Flask
    └── templates/
        └── index.html    # Interfejs webowy
```

## API Endpoints

- `GET /` - Strona główna
- `GET /api/scan` - Skanowanie plików SVG
- `GET /api/file/<path>` - Pobieranie pliku SVG
- `GET /api/preview/<path>` - Podgląd zawartości pliku

## Rozwój

### Uruchomienie w trybie debug:
```bash
# W .env ustaw:
DEBUG=True

# Uruchom serwer
poetry run python svg_browser/app.py
```

### Formatowanie kodu:
```bash
poetry run black svg_browser/
```

### Linting:
```bash
poetry run flake8 svg_browser/
```

## Rozwiązywanie problemów

### Problemy z instalacją Poetry:
```bash
# Automatyczna naprawa
python fix_install.py

# Lub ręczna naprawa
poetry cache clear --all pypi
poetry env remove python
poetry install

# Alternatywnie - użyj pip
python quick_start.py
```

### Diagnostyka:
```bash
python diagnose.py  # Sprawdzi całą instalację
```

### Szybkie rozwiązania:
```bash
make fix            # Naprawa przez Makefile
python start.py     # Interaktywny starter z diagnozą
```

## Licencja

MIT License

## Autor

Stworzony z pomocą Claude AI dla lokalnego przeglądania kolekcji plików SVG.