#!/usr/bin/env python3
"""
Simple Note-Taking PWA Server
Serves a self-contained SVG-based note-taking application
"""

import os
import json
import base64
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import threading
import webbrowser
import time


class NoteHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/' or path == '/index.html':
            self.serve_svg_app()
        elif path == '/manifest.json':
            self.serve_manifest()
        elif path == '/api/notes/export':
            self.handle_export_notes()
        elif path.startswith('/api/notes'):
            self.handle_get_notes()
        else:
            self.send_error(404)

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/api/notes':
            self.handle_save_note()
        elif path == '/api/notes/import':
            self.handle_import_notes()
        else:
            self.send_error(404)

    def serve_svg_app(self):
        """Serve the main SVG PWA application"""
        svg_content = self.get_svg_app()
        self.send_response(200)
        self.send_header('Content-Type', 'image/svg+xml')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        self.wfile.write(svg_content.encode('utf-8'))

    def serve_manifest(self):
        """Serve PWA manifest"""
        manifest = {
            "name": "NotePWA",
            "short_name": "NotePWA",
            "description": "Simple note-taking and drawing app",
            "start_url": "/",
            "display": "standalone",
            "background_color": "#ffffff",
            "theme_color": "#2196f3",
            "icons": [
                {
                    "src": "data:image/svg+xml;base64," + base64.b64encode(
                        b'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 192 192"><rect width="192" height="192" fill="#2196f3"/><path d="M48 48h96v96H48z" fill="white"/><path d="M64 64h64v8H64zm0 16h64v8H64zm0 16h48v8H64z" fill="#2196f3"/></svg>''').decode(),
                    "sizes": "192x192",
                    "type": "image/svg+xml"
                }
            ]
        }

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(manifest).encode('utf-8'))

    def handle_get_notes(self):
        """Get saved notes"""
        try:
            if os.path.exists('notes.json'):
                with open('notes.json', 'r') as f:
                    notes = json.load(f)
            else:
                notes = []

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(notes).encode('utf-8'))
        except Exception as e:
            self.send_error(500, str(e))

    def handle_export_notes(self):
        """Export all notes as a JSON file"""
        try:
            if not os.path.exists('notes.json'):
                notes = []
            else:
                with open('notes.json', 'r') as f:
                    notes = json.load(f)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Disposition', 'attachment; filename="notes_export.json"')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(notes, indent=2).encode('utf-8'))
        except Exception as e:
            self.send_error(500, str(e))

    def handle_import_notes(self):
        """Import notes from a JSON file"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            notes = json.loads(post_data.decode('utf-8'))

            # Validate the imported data
            if not isinstance(notes, list):
                raise ValueError("Invalid notes format")

            # Save the imported notes
            with open('notes.json', 'w') as f:
                json.dump(notes, f, indent=2)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'imported', 'count': len(notes)}).encode('utf-8'))
        except Exception as e:
            self.send_error(400, f"Error importing notes: {str(e)}")

    def handle_save_note(self):
        """Save a note"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            note_data = json.loads(post_data.decode('utf-8'))

            # Load existing notes
            if os.path.exists('notes.json'):
                with open('notes.json', 'r') as f:
                    notes = json.load(f)
            else:
                notes = []

            # Add timestamp
            note_data['timestamp'] = datetime.now().isoformat()
            note_data['id'] = len(notes)

            # Save note
            notes.append(note_data)

            with open('notes.json', 'w') as f:
                json.dump(notes, f, indent=2)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'saved', 'id': note_data['id']}).encode('utf-8'))

        except Exception as e:
            self.send_error(500, str(e))

    def get_svg_app(self):
        """Generate the complete SVG PWA application"""
        return '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
     width="100%" height="100%" viewBox="0 0 1200 800">

  <defs>
    <!-- Embedded CSS -->
    <style type="text/css"><![CDATA[
      .toolbar { fill: #f5f5f5; stroke: #ddd; stroke-width: 1; }
      .button { fill: #2196f3; stroke: #1976d2; stroke-width: 1; cursor: pointer; }
      .button:hover { fill: #1976d2; }
      .button-text { fill: white; font-family: Arial, sans-serif; font-size: 12px; text-anchor: middle; dominant-baseline: middle; pointer-events: none; }
      .tool-active { fill: #ff9800 !important; }
      .canvas-area { fill: white; stroke: #ddd; stroke-width: 1; }
      .text-input { font-family: Arial, sans-serif; font-size: 14px; }
      .note-item { fill: #f9f9f9; stroke: #ddd; stroke-width: 1; cursor: pointer; }
      .note-item:hover { fill: #e3f2fd; }
    ]]></style>
  </defs>

  <!-- Background -->
  <rect width="100%" height="100%" fill="#fafafa"/>

  <!-- Header Toolbar -->
  <rect class="toolbar" x="0" y="0" width="1200" height="60"/>

  <!-- Tool Buttons -->
  <g id="toolbar">
    <!-- Pen Tool -->
    <rect class="button tool-active" id="pen-btn" x="10" y="10" width="60" height="40" rx="4"/>
    <text class="button-text" x="40" y="30">Pen</text>

    <!-- Eraser Tool -->
    <rect class="button" id="eraser-btn" x="80" y="10" width="60" height="40" rx="4"/>
    <text class="button-text" x="110" y="30">Eraser</text>

    <!-- Text Tool -->
    <rect class="button" id="text-btn" x="150" y="10" width="60" height="40" rx="4"/>
    <text class="button-text" x="180" y="30">Text</text>

    <!-- Clear -->
    <rect class="button" id="clear-btn" x="220" y="10" width="60" height="40" rx="4"/>
    <text class="button-text" x="250" y="30">Clear</text>

    <!-- Save -->
    <rect class="button" id="save-btn" x="290" y="10" width="60" height="40" rx="4"/>
    <text class="button-text" x="320" y="30">Save</text>

    <!-- Export -->
    <rect class="button" id="export-btn" x="360" y="10" width="60" height="40" rx="4"/>
    <text class="button-text" x="390" y="30">Export</text>

    <!-- Import -->
    <rect class="button" id="import-btn" x="430" y="10" width="60" height="40" rx="4"/>
    <text class="button-text" x="460" y="30">Import</text>
    <input type="file" id="import-file" accept=".json" style="display: none;"/>

    <!-- Color Picker -->
    <circle id="color-picker" cx="450" cy="30" r="15" fill="#000000" stroke="#ddd" stroke-width="2"/>

    <!-- Brush Size -->
    <text class="button-text" x="490" y="25" style="fill: #333;">Size:</text>
    <circle id="size-indicator" cx="520" cy="30" r="3" fill="#333"/>
  </g>

  <!-- Main Content Area -->
  <g id="main-content">
    <!-- Drawing Canvas -->
    <rect class="canvas-area" id="canvas" x="20" y="80" width="800" height="600"/>
    <g id="drawing-layer"></g>
    <g id="text-layer"></g>

    <!-- Notes Panel -->
    <rect class="toolbar" x="840" y="80" width="340" height="600"/>
    <text x="860" y="105" style="font-family: Arial; font-size: 16px; font-weight: bold; fill: #333;">Saved Notes</text>
    <g id="notes-list" transform="translate(850, 120)"></g>
  </g>

    <!-- Hidden Elements -->
    <foreignObject x="0" y="0" width="1" height="1" style="overflow: hidden;">
      <a id="export-link" style="display: none;"></a>
    </foreignObject>
    <input type="color" id="color-input" style="opacity: 0; pointer-events: none;"/>
    <input type="range" id="size-input" min="1" max="20" value="3" style="opacity: 0; pointer-events: none;"/>
  </foreignObject>

  <script type="text/javascript"><![CDATA[
    // PWA Registration
    if ('serviceWorker' in navigator) {
      const swCode = `
        const CACHE_NAME = 'notepwa-v1';
        self.addEventListener('install', (e) => {
          e.waitUntil(
            caches.open(CACHE_NAME).then((cache) => {
              return cache.addAll(['/']);
            })
          );
        });
        self.addEventListener('fetch', (e) => {
          e.respondWith(
            caches.match(e.request).then((response) => {
              return response || fetch(e.request);
            })
          );
        });
      `;
      const blob = new Blob([swCode], { type: 'application/javascript' });
      const swUrl = URL.createObjectURL(blob);
      navigator.serviceWorker.register(swUrl);
    }

    // App State
    let currentTool = 'pen';
    let isDrawing = false;
    let currentPath = null;
    let currentColor = '#000000';
    let currentSize = 3;
    let textMode = false;
    let notes = [];

    // Elements
    const canvas = document.getElementById('canvas');
    const drawingLayer = document.getElementById('drawing-layer');
    const textLayer = document.getElementById('text-layer');
    const notesList = document.getElementById('notes-list');

    // Tool Selection
    function selectTool(tool) {
      currentTool = tool;
      textMode = (tool === 'text');

      // Update button states
      document.querySelectorAll('.button').forEach(btn => {
        btn.classList.remove('tool-active');
      });
      document.getElementById(tool + '-btn').classList.add('tool-active');

      // Update cursor
      canvas.style.cursor = textMode ? 'text' : 'crosshair';
    }

    // Drawing Functions
    function startDrawing(e) {
      if (currentTool === 'text') return;

      isDrawing = true;
      const rect = canvas.getBoundingClientRect();
      const svgRect = document.querySelector('svg').getBoundingClientRect();
      const x = e.clientX - svgRect.left - 20;
      const y = e.clientY - svgRect.top - 80;

      currentPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      currentPath.setAttribute('d', `M ${x} ${y}`);
      currentPath.setAttribute('fill', 'none');
      currentPath.setAttribute('stroke', currentTool === 'eraser' ? 'white' : currentColor);
      currentPath.setAttribute('stroke-width', currentTool === 'eraser' ? currentSize * 3 : currentSize);
      currentPath.setAttribute('stroke-linecap', 'round');
      currentPath.setAttribute('stroke-linejoin', 'round');

      drawingLayer.appendChild(currentPath);
    }

    function draw(e) {
      if (!isDrawing || currentTool === 'text') return;

      const rect = canvas.getBoundingClientRect();
      const svgRect = document.querySelector('svg').getBoundingClientRect();
      const x = e.clientX - svgRect.left - 20;
      const y = e.clientY - svgRect.top - 80;

      const d = currentPath.getAttribute('d');
      currentPath.setAttribute('d', d + ` L ${x} ${y}`);
    }

    function stopDrawing() {
      isDrawing = false;
      currentPath = null;
    }

    // Text Functions
    function addText(e) {
      if (currentTool !== 'text') return;

      const rect = canvas.getBoundingClientRect();
      const svgRect = document.querySelector('svg').getBoundingClientRect();
      const x = e.clientX - svgRect.left - 20;
      const y = e.clientY - svgRect.top - 80;

      const text = prompt('Enter text:');
      if (text) {
        const textElement = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        textElement.setAttribute('x', x);
        textElement.setAttribute('y', y);
        textElement.setAttribute('fill', currentColor);
        textElement.setAttribute('font-size', currentSize * 4);
        textElement.setAttribute('font-family', 'Arial, sans-serif');
        textElement.textContent = text;
        textLayer.appendChild(textElement);
      }
    }

    // Save/Load Functions
    function saveNote() {
      const drawingData = drawingLayer.innerHTML;
      const textData = textLayer.innerHTML;
      const timestamp = new Date().toISOString();

      const noteData = {
        drawing: drawingData,
        text: textData,
        timestamp: timestamp,
        title: prompt('Note title:', 'Note ' + (notes.length + 1))
      };

      fetch('/api/notes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(noteData)
      })
      .then(response => response.json())
      .then(data => {
        console.log('Note saved:', data);
        loadNotes();
      })
      .catch(error => console.error('Error saving note:', error));
    }
    
    // Export notes to a JSON file
    function exportNotes() {
      fetch('/api/notes/export')
        .then(response => response.blob())
        .then(blob => {
          const url = window.URL.createObjectURL(blob);
          const a = document.getElementById('export-link');
          a.href = url;
          a.download = 'notes_export.json';
          a.click();
          window.URL.revokeObjectURL(url);
        })
        .catch(error => alert('Error exporting notes: ' + error));
    }
    
    // Import notes from a JSON file
    function importNotes(event) {
      const file = event.target.files[0];
      if (!file) return;
      
      const reader = new FileReader();
      reader.onload = function(e) {
        try {
          const notesData = JSON.parse(e.target.result);
          
          // Send the notes to the server
          fetch('/api/notes/import', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(notesData)
          })
          .then(response => response.json())
          .then(data => {
            alert(`Successfully imported ${data.count} notes`);
            loadNotes(); // Reload the notes list
          })
          .catch(error => alert('Error importing notes: ' + error));
        } catch (e) {
          alert('Invalid JSON file: ' + e.message);
        }
      };
      reader.readAsText(file);
      
      // Reset the file input so the same file can be imported again
      event.target.value = '';
    }

    // Add event listeners for import/export buttons
    document.getElementById('export-btn').addEventListener('click', exportNotes);
    document.getElementById('import-btn').addEventListener('click', () => {
      document.getElementById('import-file').click();
    });
    document.getElementById('import-file').addEventListener('change', importNotes);)
      .then(data => {
        notes = data;
        renderNotesList();
      })
      .catch(error => console.error('Error loading notes:', error));
    }

    function renderNotesList() {
      notesList.innerHTML = '';

      notes.forEach((note, index) => {
        const noteItem = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        noteItem.setAttribute('transform', `translate(0, ${index * 60})`);

        const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        rect.setAttribute('class', 'note-item');
        rect.setAttribute('width', '320');
        rect.setAttribute('height', '50');
        rect.setAttribute('rx', '4');

        const title = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        title.setAttribute('x', '10');
        title.setAttribute('y', '20');
        title.setAttribute('font-family', 'Arial, sans-serif');
        title.setAttribute('font-size', '14');
        title.setAttribute('font-weight', 'bold');
        title.textContent = note.title || 'Untitled Note';

        const date = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        date.setAttribute('x', '10');
        date.setAttribute('y', '35');
        date.setAttribute('font-family', 'Arial, sans-serif');
        date.setAttribute('font-size', '10');
        date.setAttribute('fill', '#666');
        date.textContent = new Date(note.timestamp).toLocaleString();

        noteItem.appendChild(rect);
        noteItem.appendChild(title);
        noteItem.appendChild(date);

        noteItem.addEventListener('click', () => loadNote(index));
        notesList.appendChild(noteItem);
      });
    }

    function loadNote(index) {
      const note = notes[index];
      drawingLayer.innerHTML = note.drawing || '';
      textLayer.innerHTML = note.text || '';
    }

    function clearCanvas() {
      drawingLayer.innerHTML = '';
      textLayer.innerHTML = '';
    }

    // Event Listeners
    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('click', addText);

    // Tool buttons
    document.getElementById('pen-btn').addEventListener('click', () => selectTool('pen'));
    document.getElementById('eraser-btn').addEventListener('click', () => selectTool('eraser'));
    document.getElementById('text-btn').addEventListener('click', () => selectTool('text'));
    document.getElementById('clear-btn').addEventListener('click', clearCanvas);
    document.getElementById('save-btn').addEventListener('click', saveNote);
    document.getElementById('export-btn').addEventListener('click', exportNotes);
    document.getElementById('import-btn').addEventListener('click', () => {
      document.getElementById('import-file').click();
    });
    document.getElementById('import-file').addEventListener('change', importNotes);

    // Color picker
    document.getElementById('color-picker').addEventListener('click', () => {
      const input = document.getElementById('color-input');
      input.click();
      input.addEventListener('change', (e) => {
        currentColor = e.target.value;
        document.getElementById('color-picker').setAttribute('fill', currentColor);
      }, { once: true });
    });

    // Size control
    document.getElementById('size-indicator').addEventListener('click', () => {
      const input = document.getElementById('size-input');
      input.style.opacity = '1';
      input.style.position = 'absolute';
      input.style.left = '500px';
      input.style.top = '20px';
      input.focus();

      input.addEventListener('input', (e) => {
        currentSize = parseInt(e.target.value);
        document.getElementById('size-indicator').setAttribute('r', currentSize);
      });

      input.addEventListener('blur', () => {
        input.style.opacity = '0';
        input.style.position = 'static';
      }, { once: true });
    });

    // Initialize
    loadNotes();
    selectTool('pen');

    // PWA Install prompt
    let deferredPrompt;
    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      deferredPrompt = e;
    });
  ]]></script>
</svg>'''


def open_browser():
    """Open browser after short delay"""
    time.sleep(1)
    webbrowser.open('http://localhost:8000')


def main():
    server_address = ('localhost', 8000)
    httpd = HTTPServer(server_address, NoteHandler)

    print("Starting NotePWA Server...")
    print(f"Server running at http://localhost:8000")
    print("Press Ctrl+C to stop the server")

    # Open browser in background thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.shutdown()


if __name__ == '__main__':
    main()