# NotePWA - Node.js Edition

Prosta aplikacja PWA (Progressive Web App) do robienia notatek i rysowania, oparta na SVG z backendem w Node.js.

## 🎯 Funkcje

### 🎨 Narzędzia do rysowania (inspirowane Rnote)
- **Pióro** - swobodne rysowanie
- **Gumka** - usuwanie pociągnięć
- **Regulacja rozmiaru pędzla** (1-20px)
- **Wybór kolorów** - pełna paleta kolorów
- **Rysowanie wektorowe** na kanwie SVG

### 📝 Zarządzanie notatkami (inspirowane OneNote)
- **Narzędzie tekstowe** - dodawanie tekstu
- **Zapisywanie notatek** z niestandardowymi tytułami
- **Ładowanie i organizacja** zapisanych notatek
- **Panel notatek** z podglądem wszystkich notatek i znacznikami czasu
- **Usuwanie notatek** - pojedyncze kliknięcie X

### 📱 Możliwości PWA
- **Kompletna Progressive Web App**
- **Service Worker** dla funkcji offline
- **Możliwość instalacji** na desktop/mobile
- **Samostawne SVG** z wbudowanym CSS/JavaScript
- **Obsługa dotykowa** dla urządzeń mobilnych

### ⌨️ Skróty klawiszowe
- **Ctrl+S** - Zapisz notatkę
- **Ctrl+N** - Nowa notatka
- **Ctrl+L** - Załaduj notatki
- **1** - Narzędzie pióra
- **2** - Gumka
- **3** - Narzędzie tekstowe

## 🚀 Instalacja i uruchomienie

### Wymagania
- Node.js >= 14.0.0
- npm lub yarn

### Szybki start

1. **Skopiuj pliki:**
   ```bash
   # Utwórz katalog projektu
   mkdir notepwa-nodejs
   cd notepwa-nodejs
   
   # Skopiuj server.js i package.json
   ```

2. **Zainstaluj zależności:**
   ```bash
   npm install
   ```

3. **Uruchom serwer:**
   ```bash
   npm start
   ```

4. **Aplikacja otwiera się automatycznie** w przeglądarce pod adresem `http://localhost:8000`

### Tryb rozwoju (z auto-restartowaniem)
```bash
npm run dev
```

## 📖 Jak używać

### Podstawowe funkcje:
1. **Rysowanie**: Wybierz narzędzie pióra (1) i rysuj na białej kanwie
2. **Gumka**: Wybierz gumkę (2) aby usuwać pociągnięcia
3. **Dodawanie tekstu**: Wybierz narzędzie tekstowe (3) i kliknij w miejsce gdzie chcesz dodać tekst
4. **Zmiana kolorów**: Kliknij kolorowe kółko aby wybrać kolor
5. **Rozmiar pędzla**: Kliknij wskaźnik rozmiaru aby zmienić grubość pędzla

### Zarządzanie notatkami:
- **Zapisz**: Kliknij "Save" aby zapisać swoją pracę z niestandardowym tytułem
- **Nowa**: Kliknij "New" aby rozpocząć nową notatkę
- **Załaduj**: Kliknij "Load" aby zobaczyć wszystkie zapisane notatki
- **Otwórz notatkę**: Kliknij na dowolną notatkę w panelu po prawej stronie
- **Usuń notatkę**: Kliknij "✕" na notatce którą chcesz usunąć

### Obsługa mobilna:
- Aplikacja w pełni obsługuje dotyk
- Możesz rysować palcem na urządzeniach dotykowych
- Wszystkie funkcje działają na telefonach i tabletach

## 🗂️ Struktura plików

```
notepwa-nodejs/
├── server.js          # Główny serwer Node.js
├── package.json       # Konfiguracja npm
├── notes.json         # Plik z zapisanymi notatkami (tworzony automatycznie)
└── README.md          # Ta dokumentacja
```

## 🔧 Szczegóły techniczne

### Backend (Node.js + Express):
- **Express.js** - serwer HTTP
- **REST API** do zarządzania notatkami
- **Przechowywanie w JSON** - wszystkie notatki w `notes.json`
- **CORS** - obsługa requestów cross-origin
- **Automatyczne otwieranie przeglądarki**

### Frontend (SVG + JavaScript):
- **Jedna plik SVG** z wbudowanym CSS i JavaScript
- **Service Worker** dla funkcji PWA
- **Canvas SVG** do rysowania wektorowego
- **Touch events** dla urządzeń mobilnych
- **Local Storage** dla cache'owania

### API Endpoints:
- `GET /` - Główna aplikacja SVG
- `GET /manifest.json` - Manifest PWA
- `GET /api/notes` - Pobierz wszystkie notatki
- `POST /api/notes` - Zapisz nową notatkę
- `DELETE /api/notes/:id` - Usuń notatkę

## 🌟 Funkcje zaawansowane

### PWA Install:
- Aplikacja może być zainstalowana jako natywna aplikacja
- Działa offline dzięki Service Worker
- Ikona aplikacji i splash screen

### Responsywność:
- Automatyczne dostosowanie do różnych rozmiarów ekranu
- Obsługa orientacji pionowej i poziomej
- Optymalizacja dla tabletów i telefonów

### Wydajność:
- Rysowanie wektorowe SVG - skalowalność bez utraty jakości
- Minimalne zużycie pamięci
- Szybkie ładowanie dzięki embedded assets

## 🤝 Rozszerzanie

Możesz łatwo rozszerzyć aplikację o:
- Więcej narzędzi rysowania (kształty, linie)
- Warstwy i grupowanie elementów
- Export do PDF/PNG
- Synchronizacja w chmurze
- Współpraca w czasie rzeczywistym

## 📄 Licencja

MIT License - możesz używać, modyfikować i dystrybuować kod zgodnie z potrzebami.

## 🔍 Rozwiązywanie problemów

**Port zajęty:**
```bash
# Zmień port w server.js (linia: const PORT = 8000)
```

**Notatki nie zapisują się:**
```bash
# Sprawdź uprawnienia do zapisu w katalogu
chmod 755 .
```

**Aplikacja nie otwiera się:**
```bash
# Sprawdź czy Node.js jest zainstalowany
node --version
npm --version
```

---

**Stworzone z ❤️ używając Node.js, Express, SVG i czystego JavaScript**