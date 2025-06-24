# PWA.SVG Example Application

This directory contains example Progressive Web Applications built entirely within SVG files. Each `.pwa.svg` file is a complete, self-contained application.

# Notes PWA.SVG Application

A simple note-taking application built entirely within an SVG file using PWA capabilities.

## Features

- Create and edit notes
- Auto-saves notes to localStorage
- Responsive design
- Works offline
- Installable as a PWA

## Usage

1. Open `note.pwa.svg` in a modern web browser
2. Start typing to create a new note
3. Your notes are automatically saved

## Development

### Dependencies

- Modern web browser
- Node.js 14+ (for testing)

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

- `saveNote(text)` - Saves the note to localStorage
- `loadNote()` - Loads the note from localStorage

## License

[Your License Here]
