# Markdown Editor PWA

Nowoczesny edytor Markdown w formie PWA (Progressive Web App) z podglądem w czasie rzeczywistym i zaawansowanymi funkcjami eksportu.

## ✨ Funkcje

- **Edytor Markdown** z podświetlaniem składni
- **Podgląd na żywo** z renderowaniem HTML
- **Eksport do plików**
  - Pobierz jako Markdown (.md)
  - Eksportuj do HTML (.html)
- **Funkcje schowka**
  - Kopiuj HTML (czysty)
  - Kopiuj HTML z wbudowanym CSS
- **Pełna obsługa PWA**
  - Działa offline
  - Możliwość instalacji na urządzeniu
  - Szybkie ładowanie

## 🚀 Uruchomienie lokalnie

1. Upewnij się, że masz zainstalowany serwer HTTP (np. Python, PHP, Node.js)

2. Uruchom serwer w katalogu projektu:

   **Z Pythonem 3:**
   ```bash
   python3 -m http.server 8000
   ```

   **Z PHP:**
   ```bash
   php -S localhost:8000
   ```

3. Otwórz przeglądarkę i przejdź do:
   ```
   http://localhost:8000/edit.svg
   ```

## 📝 Użycie

1. Wpisz tekst Markdown w lewym panelu
2. Oglądaj podgląd HTML po prawej stronie
3. Użyj przycisków w górnym pasku, aby:
   - Pobrać plik Markdown
   - Wyeksportować do HTML
   - Skopiować HTML do schowka
   - Wyczyścić edytor

## 📱 Obsługa PWA

Aplikacja obsługuje instalację jako PWA:
1. Otwórz w Chrome/Edge/Opera na komputerze
2. Kliknij ikonę instalacji w pasku adresu
3. Albo użyj menu przeglądarki (Chrome: ⋮ → Zainstaluj...)

## 🛠️ Technologie

- Czyste HTML5, CSS3 i JavaScript (ES6+)
- Service Worker do obsługi offline
- Web Share API do udostępniania
- LocalStorage do zapisywania postępu

## 📄 Licencja

MIT License - dowolne wykorzystanie dozwolone z zachowaniem informacji o autorstwie.

---

**Stworzone z ❤️ przy użyciu czystego JavaScript i SVG**