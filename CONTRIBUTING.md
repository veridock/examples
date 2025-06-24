# Contributing to PWA.SVG Applications

Welcome! We're excited you're interested in contributing to our PWA.SVG applications. This guide will help you get started with development.

## What are PWA.SVG Applications?

PWA.SVG applications are Progressive Web Apps built entirely within a single SVG file. They combine:
- **SVG** for vector graphics and layout
- **HTML5** for structure (using foreignObject)
- **CSS** for styling
- **JavaScript** for interactivity
- **PWA** capabilities for offline functionality

## Getting Started

### Prerequisites

- Modern web browser (Chrome, Firefox, Edge, or Safari)
- Code editor (VS Code, Sublime Text, etc.)
- Node.js 14+ (for development tools)
- Git (for version control)

### Project Structure

```
veridock/
├── examples/           # Example PWA.SVG applications
│   ├── note.pwa.svg    # Notes application
│   ├── qrgen.pwa.svg   # QR Code Generator
│   └── stoper.pwa.svg  # Stopwatch
├── tests/              # Test files
├── CONTRIBUTING.md     # This file
└── README.md          # Project documentation
```

## Development Guide

### Creating a New PWA.SVG App

1. **Start with a basic template**:
   ```svg
   <?xml version="1.0" encoding="UTF-8"?>
   <svg xmlns="http://www.w3.org/2000/svg" 
        xmlns:xhtml="http://www.w3.org/1999/xhtml"
        viewBox="0 0 400 600">
     
     <!-- Your SVG content here -->
     
     <!-- Use foreignObject to embed HTML content -->
     <foreignObject x="0" y="0" width="100%" height="100%">
       <xhtml:div style="width: 100%; height: 100%;">
         <!-- Your HTML/CSS/JavaScript here -->
       </xhtml:div>
     </foreignObject>
     
     <!-- Add JavaScript -->
     <script><![CDATA[
       // Your JavaScript code here
     ]]></script>
   </svg>
   ```

2. **Key Development Practices**:
   - Keep all code in a single .svg file
   - Use `foreignObject` to embed HTML content
   - Use inline styles or `<style>` tags for CSS
   - Place JavaScript in a `<script>` tag with CDATA
   - Use `xhtml:` prefix for HTML elements

### Running the Applications

1. **Local Development**:
   ```bash
   # Start a local server
   python3 -m http.server 8000
   ```
   Then open `http://localhost:8000/examples/your-app.pwa.svg` in your browser.

2. **Testing**:
   ```bash
   cd tests/e2e
   npm install
   npm test
   ```

## Best Practices

### SVG Structure
- Keep the viewBox consistent (e.g., `0 0 400 600`)
- Use relative units (%, em) for better responsiveness
- Group related elements with `<g>` tags
- Add proper ARIA attributes for accessibility

### JavaScript
- Use ES6+ features
- Keep the global namespace clean
- Add error handling
- Use event delegation for better performance
- Implement service workers for offline functionality

### Styling
- Use CSS variables for theming
- Keep styles scoped to components
- Use SVG filters and gradients for visual effects
- Ensure proper contrast for accessibility

## Testing

We use Playwright for end-to-end testing. To run tests:

```bash
cd tests/e2e
npm test
```

Test files should be placed in `tests/e2e/specs/` following the naming convention `*.spec.js`.

## Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Code Review Process

1. Ensure all tests pass
2. Update documentation as needed
3. Ensure your code follows the project's style guide
4. Request review from at least one maintainer

## License

By contributing, you agree that your contributions will be licensed under the project's [LICENSE](LICENSE) file.

---

Thank you for your interest in contributing! If you have any questions, please open an issue.
