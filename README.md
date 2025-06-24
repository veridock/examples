# Veridock PWA.SVG Applications

A collection of Progressive Web Applications (PWAs) built entirely within SVG files. Each application is a single, self-contained `.svg` file that includes HTML, CSS, and JavaScript.

plik #SVG + funkcje #PWA = #veriDock - Kompaktowa aplikacja w jednym pliku SVG
+ Minimalistyczny rozmiar i elastyczność SVG z zaawansowaną funkcjonalnością PWA, tworząc nowoczesną, łatwą w użyciu aplikację, działającą zarówno offline, jak i online.
+ Lekka, łatwa do przesyłania (np. przez email) oraz kompatybilna z nowoczesnymi przeglądarkami.

Dzięki temu rozwiązaniu użytkownicy nie muszą pobierać dodatkowych zasobów z zewnętrznych serwerów, co przyspiesza ładowanie aplikacji.

Pełna funkcjonalność PWA

Integracja z funkcjami Progressive Web App (PWA), w tym Service Worker (offline, cache), App Manifest (instalacja, ikony, skróty), powiadomienia, wskaźniki online/offline oraz wsparcie dla funkcji takich jak Wake Lock i Badging API.

Umożliwia instalację aplikacji na urządzeniach mobilnych, automatyczne działanie offline, przechowywanie stanu aplikacji między sesjami oraz otrzymywanie powiadomień systemowych.

Zaawansowane funkcje interaktywne i analityczne
Wbudowane animacje SVG, efekty hover, skróty klawiaturowe, śledzenie użytkowania (Analytics), eksportowanie wyników oraz monitorowanie wydajności aplikacji.

Obsługuje dynamiczne aktualizacje w czasie rzeczywistym, responsywny design, przywracanie stanu po restarcie oraz wymianę danych z innymi aplikacjami.


## 📱 Featured Applications

### 1. 📝 Notes App
A simple note-taking application with auto-save functionality and local storage.
- [View App](note/note.pwa.svg)
- [Documentation](note/README.md)

### 2. 🔳 QR Code Generator
Generate and customize QR codes from text or URLs with real-time preview.
- [View App](qrgen/qrgen.pwa.svg)
- [Documentation](qrgen/README.md)

### 3. ⏱️ Basic Stopwatch
A simple stopwatch with second-precision timing and clean interface.
- Start/Stop and Reset functionality
- Progress ring visualization
- Minimalist design
- [View App](stoper/stoper.pwa.svg)
- [Documentation](stoper/README.md)

### 4. ⏱️ Enhanced Stopwatch (PWA)
Feature-rich stopwatch with millisecond precision and PWA capabilities.
- Start/Stop, Reset, and Lap functionality
- Millisecond precision timing
- Animated progress rings (seconds and minutes)
- PWA features (installable, works offline)
- Modern gradient UI with smooth animations
- [View App](stoper2/stoper.pwa.svg)
- [HTML Version](stoper2/stoper.pwa.html)

### 5. ⏱️ Premium Stopwatch (Advanced)
Advanced stopwatch with additional features for power users.
- All features from Enhanced version
- Multiple timer presets
- Theme support (light/dark mode)
- Advanced analytics and statistics
- Export/Import functionality
- [View App](stoper3/stoper.pwa.svg)
- [HTML Version](stoper3/stoper.pwa.html)

## 🚀 Getting Started

### Prerequisites
- Modern web browser (Chrome, Firefox, Edge, or Safari)
- Optional: Node.js 14+ for development and testing

### Running Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/veridock.git
   cd veridock
   ```

2. Start a local server:
   ```bash
   python3 -m http.server 8000
   ```

3. Open any application in your browser:
   ```
   http://localhost:8000/examples/note/note.pwa.svg
   http://localhost:8000/examples/qrgen/qrgen.pwa.svg
   http://localhost:8000/examples/stoper/stoper.pwa.svg
   http://localhost:8000/examples/stoper2/stoper.pwa.svg
   http://localhost:8000/examples/stoper3/stoper.pwa.svg
   ```

## 🧪 Testing

### Unit Tests
Run unit tests for a specific application:
```bash
# Run tests for all applications
cd examples/note && node test.js
cd examples/qrgen && node test.js
cd examples/stoper && node test.js
cd examples/stoper2 && node test.js
cd examples/stoper3 && node test.js

# Or run all tests from the root directory
make test
```

### End-to-End Testing
Run Playwright tests:
```bash
cd tests/e2e
npm install
npm test
```

## 🛠️ Development

### Project Structure
```
veridock/
├── examples/           # Example PWA.SVG applications
│   ├── note/           # 📝 Notes application
│   ├── qrgen/          # 🔳 QR Code Generator
│   ├── stoper/         # ⏱️ Basic Stopwatch
│   ├── stoper2/        # ⏱️ Enhanced Stopwatch with PWA features
│   └── stoper3/        # ⏱️ Premium Stopwatch with analytics
├── tests/              # Test files
├── docs/               # Documentation
└── CONTRIBUTING.md     # Contribution guidelines
```

### Creating a New PWA.SVG App
1. Create a new directory in `examples/`
2. Create your `.pwa.svg` file with the following structure:
   ```svg
   <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 600">
     <!-- SVG content -->
     <foreignObject width="100%" height="100%">
       <xhtml:div>
         <!-- Your HTML/CSS/JS here -->
       </xhtml:div>
     </foreignObject>
     <script><![CDATA[
       // Your JavaScript here
     ]]></script>
   </svg>
   ```
3. Add tests in a `test.js` file
4. Update this README with your new application

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on how to contribute to this project.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Contact

For questions or feedback, please open an issue on GitHub.

---

https://www.pwabuilder.com/imagegenerator

Built with ❤️ by the Veridock Team
