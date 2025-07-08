# NotePWA - Instrukcje instalacji

Kompletna aplikacja PWA do robienia notatek i rysowania z dwoma backendami: **Python** i **Node.js**.

## 📁 Struktura plików

Po pobraniu wszystkich plików, struktura katalogów powinna wyglądać tak:

```
notepwa/
├── notepwa.svg          # 🎨 Wspólna aplikacja SVG (frontend)
├── note_server.py       # 🐍 Serwer Python 
├── server.js            # 🟢 Serwer Node.js
├── package.json         # 📦 Konfiguracja npm
├── notes.svg            # 💾 Baza danych w formie visual grid (tworzona automatycznie)
├── test_svg.py          # 🧪 Validator SVG
└── test_backends.py     # 🧪 Test kompatybilności
```

## 🎯 Opcja 1: Python Backend

### Wymagania:
- Python 3.7+
- Żadnych dodatkowych bibliotek (używa standardowych modułów)

### Uruchomienie:
```bash
# Przejdź do katalogu z plikami
cd notepwa

# Uruchom serwer Python
python note_server.py
```

✅ **Przeglądarka otworzy się automatycznie na** `http://localhost:8000`

## 🟢 Opcja 2: Node.js Backend  

### Wymagania:
- Node.js 14+
- npm

### Instalacja i uruchomienie:
```bash
# Przejdź do katalogu z plikami
cd notepwa

# Zainstaluj zależności
npm install

# Uruchom serwer Node.js
npm start
```

✅ **Przeglądarka otworzy się automatycznie na** `http://localhost:8000`

### Tryb development (z auto-restart):
```bash
npm run dev
```

## 🎨 Co robi plik `notepwa.svg`?

**To jest serce aplikacji!** Jeden plik zawiera:
- ✨ Kompletny interface użytkownika
- 🎨 Narzędzia do rysowania (pióro, gumka, kolory)
- 📝 System zarządzania notatkami  
- 📱 Funkcje PWA (Progressive Web App)
- ⌨️ Skróty klawiszowe
- 📱 Obsługa touch dla mobile

## 🔄 Jak to działa?

1. **Wspólny frontend**: Oba serwery serwują ten sam plik `notepwa.svg`
2. **Identyczne API**: Oba backendy mają identyczne endpointy REST
3. **Automatyczna detekcja**: Aplikacja wykrywa jaki backend jest używany
4. **Wspólna baza**: Oba serwery używają tego samego pliku `notes.json`

## 🚀 Funkcje aplikacji

### 🎨 Narzędzia rysowania:
- **Pióro** - swobodne rysowanie wektorowe
- **Gumka** - usuwanie elementów
- **Kolory** - pełna paleta kolorów
- **Rozmiary** - regulacja grubości pędzla (1-20px)

### 📝 Zarządzanie notatkami:
- **Tekst** - dodawanie napisów
- **Zapisz** - zapisywanie z niestandardowymi tytułami
- **Załaduj** - przeglądanie wszystkich notatek
- **Usuń** - usuwanie niepotrzebnych notatek
- **Nowa** - tworzenie nowej notatki
- **Grid View** - wizualny podgląd wszystkich notatek w formie siatki
- **Eksport SVG** - pobieranie pojedynczych notatek jako pliki SVG

### ⌨️ Skróty klawiszowe:
- **Ctrl+S** - Zapisz notatkę
- **Ctrl+N** - Nowa notatka  
- **Ctrl+L** - Załaduj notatki
- **Ctrl+G** - Przełącz widok siatki (Grid View)
- **Ctrl+E** - Eksportuj aktualną notatkę
- **1** - Narzędzie pióra
- **2** - Gumka
- **3** - Narzędzie tekstowe

### 📱 PWA Features:
- **Offline** - działa bez internetu po pierwszym załadowaniu
- **Instalowalność** - można zainstalować jako aplikacja
- **Mobile** - pełna obsługa dotykowa
- **Responsive** - dostosowuje się do rozmiaru ekranu

## 🔧 API Endpoints (oba serwery)

```
GET  /                         # Główna aplikacja SVG
GET  /notes.svg               # Visual grid wszystkich notatek
GET  /manifest.json           # Manifest PWA  
GET  /api/info                # Informacje o backendzie
GET  /api/notes               # Lista wszystkich notatek (JSON)
POST /api/notes               # Zapisz nową notatkę
DELETE /api/notes/:id         # Usuń notatkę
GET  /api/notes/export/:id    # Eksportuj notatkę jako SVG
```

## 🔄 Przełączanie między backendami

Możesz łatwo przełączać się między Python a Node.js:

1. **Zatrzymaj aktualny serwer** (Ctrl+C)
2. **Uruchom drugi serwer**
3. **Odśwież przeglądarkę**

Wszystkie notatki będą zachowane, bo oba serwery używają tego samego pliku `notes.svg`!

## 🎨 Innowacyjne przechowywanie w SVG

### 💡 **Dlaczego notes.svg zamiast JSON?**
- **Visual Preview** - Zobacz wszystkie notatki jako miniaturki w jednym pliku
- **Self-contained** - Jeden plik SVG zawiera dane + podgląd
- **Scalable** - Możliwość bezstratnego skalowania podglądów
- **Clickable** - Interaktywny grid z możliwością kliknięcia w notatki
- **Exportable** - Łatwy eksport pojedynczych notatek

### 📂 **Struktura notes.svg:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800">
  <!-- NOTES_DATA: [{"title":"Note 1","drawing":"...","text":"..."}] -->
  
  <!-- Visual grid with note previews -->
  <rect class="note-preview" x="20" y="100" width="280" height="200"/>
  <!-- Scaled down note content -->
  <g transform="scale(0.3)">
    <!-- Actual note drawing and text -->
  </g>
  <!-- Export buttons for each note -->
</svg>
```

### 🔄 **Jak rozdzielić notes.svg na pojedyncze notatki:**

1. **Przez aplikację** - kliknij przycisk "Export" przy każdej notatce
2. **Przez API** - `GET /api/notes/export/{id}` pobiera pojedynczą notatkę SVG
3. **Przez kod** - parsuj metadane JSON z komentarzy SVG

### 🔄 **Migracja z notes.json:**
```bash
# Jeśli masz stary plik notes.json, konwertuj go:
python convert_json_to_svg.py

# Lub z custom plikami:
python convert_json_to_svg.py old_notes.json new_notes.svg
```

### 📥 **Przykład eksportu pojedynczej notatki:**
```bash
# Pobierz notatkę nr 0 jako SVG
curl http://localhost:8000/api/notes/export/0 > my_note.svg

# Otwórz w przeglądarce lub edytorze SVG
```

## 🎯 Testowanie różnic

### Python backend:
- ⚡ **Szybki start** - brak instalacji zależności
- 🔧 **Prostota** - standardowe biblioteki Python
- 📦 **Lekki** - minimalne zużycie pamięci

### Node.js backend:  
- 🚀 **Wydajność** - szybki Express.js
- 🛠️ **Ecosystem** - npm packages
- 🔄 **Development** - hot reload z nodemon

## 🐛 Rozwiązywanie problemów

### `XML Parsing Error: not well-formed`
```bash
# Sprawdź czy SVG jest poprawny
python test_svg.py

# Upewnij się, że używasz UTF-8 encoding
file notepwa.svg
```

### `notepwa.svg not found`
Upewnij się, że plik `notepwa.svg` jest w tym samym katalogu co serwer.

### Port zajęty (Address already in use)
```bash
# Znajdź proces na porcie 8000
lsof -i :8000

# Zabij proces
kill -9 <PID>
```

### Python: `ModuleNotFoundError`
```bash
# Sprawdź wersję Python
python --version

# Upewnij się, że używasz Python 3.7+
python3 note_server.py
```

### Node.js: `Cannot find module`
```bash
# Reinstaluj zależności
rm -rf node_modules package-lock.json
npm install
```

### Problemy z kodowaniem na Windows
```bash
# Użyj UTF-8 encoding
chcp 65001
python note_server.py
```

## 🌟 Rozszerzanie aplikacji

Chcesz dodać nowe funkcje? Edytuj plik `notepwa.svg`:

- **Nowe narzędzia** - dodaj przyciski w sekcji `<g id="toolbar">`
- **Stylowanie** - modyfikuj CSS w sekcji `<style>`
- **Logika** - rozszerz JavaScript w sekcji `<script>`
- **API** - dodaj nowe endpointy w obu serwerach

## 📄 Licencja

MIT License - używaj, modyfikuj i dystrybuuj zgodnie z potrzebami.

---

**🎉 Gotowe! Wybierz swój backend i zacznij tworzyć notatki!**