# QR Code Generator PWA.SVG Application

A QR code generator application built entirely within an SVG file using PWA capabilities.

## Features

- Generate QR codes from text input
- Real-time QR code generation
- Copy to clipboard functionality
- Responsive design
- Works offline
- Installable as a PWA

## Usage

1. Open `qrgen.pwa.svg` in a modern web browser
2. Enter the text or URL you want to encode
3. Click "Generate QR" to create the QR code
4. Click on the QR code to copy it to clipboard

## Development

### Dependencies

- Modern web browser
- Node.js 14+ (for testing)
- QR Code generation library (included in the SVG)

### Testing

Run unit tests:
```bash
node test.js
```

Run Playwright end-to-end tests:
```bash
npm test
```

## API

### Methods

- `generateQR(text)` - Generates a QR code for the given text
- `copyToClipboard(text)` - Copies text to clipboard

## License

[Your License Here]
