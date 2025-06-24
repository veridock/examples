# Veridock PWA.SVG Applications

A collection of Progressive Web Applications (PWAs) built entirely within SVG files. Each application is a single, self-contained `.svg` file that includes HTML, CSS, and JavaScript.
+ PWA inside SVG file
+ PWA based on SVG file
+ HTML inside SVG file
+ HTML based on SVG file

## 📱 Featured Applications

### 1. 📝 Notes App
A simple note-taking application with auto-save functionality.
- [View App](note/note.pwa.svg)
- [Documentation](note/README.md)

### 2. 🔳 QR Code Generator
Generate QR codes from text or URLs.
- [View App](qrgen/qrgen.pwa.svg)
- [Documentation](qrgen/README.md)

### 3. ⏱️ Stopwatch
A precise stopwatch with lap time functionality.
- [View App](stoper/stoper.pwa.svg)
- [Documentation](stoper/README.md)

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
   ```

## 🧪 Testing

### Unit Tests
Run unit tests for a specific application:
```bash
cd examples/note && node test.js
cd examples/qrgen && node test.js
cd examples/stoper && node test.js
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
│   ├── note/           # Notes application
│   ├── qrgen/          # QR Code Generator
│   └── stoper/         # Stopwatch
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
