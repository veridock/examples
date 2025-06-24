# Stopwatch PWA.SVG Application

A stopwatch application built entirely within an SVG file using PWA capabilities.

## Features

- Start, stop, and reset functionality
- Lap time tracking
- Responsive design
- Works offline
- Installable as a PWA
- Smooth animation

## Usage

1. Open `stoper.pwa.svg` in a modern web browser
2. Use the controls:
   - **START**: Begin timing
   - **STOP**: Pause the stopwatch
   - **RESET**: Reset the timer to zero
   - **LAP**: Record the current lap time

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

- `start()` - Starts the stopwatch
- `stop()` - Stops the stopwatch
- `reset()` - Resets the stopwatch
- `lap()` - Records a lap time

## License

[Your License Here]
