# examples

# PWA.SVG Example Applications

This directory contains example Progressive Web Applications built entirely within SVG files. Each `.pwa.svg` file is a complete, self-contained application.

## Available Examples

1. **Notes App** (`note.pwa.svg`)
   - A simple note-taking application
   - Features: Create, edit, and persist notes
   - [View Live](note/note.pwa.svg)

2. **QR Code Generator** (`qrgen.pwa.svg`)
   - Generate QR codes from text input
   - Features: Real-time generation, copy to clipboard
   - [View Live](qrgen/qrgen.pwa.svg)

3. **Stopwatch** (`stoper.pwa.svg`)
   - A functional stopwatch with start/stop/reset
   - Features: Lap time tracking, responsive design
   - [View Live](stoper/stoper.pwa.svg)

## Running the Examples

### Local Development

1. Start a local server:
   ```bash
   python3 -m http.server 8000
   ```

2. Open any example in your browser:
   ```
   http://localhost:8000/note.pwa.svg
   http://localhost:8000/qrgen.pwa.svg
   http://localhost:8000/stoper.pwa.svg
   ```

### Testing

Run the test suite:

```bash
cd tests/e2e
npm install
npm test
```

## How They Work

These applications use SVG's `foreignObject` to embed HTML content within an SVG, combined with JavaScript for interactivity. Key features:

- **Single File**: Each app is entirely self-contained in one `.svg` file
- **Progressive Enhancement**: Works in modern browsers
- **Offline Capable**: Can be installed as a PWA (Progressive Web App)
- **Responsive**: Adapts to different screen sizes

## Creating Your Own PWA.SVG

See the [CONTRIBUTING.md](../CONTRIBUTING.md) for a guide on creating your own PWA.SVG applications.

## License

[Your License Here]
