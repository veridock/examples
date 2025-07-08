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
        elif path.startswith('/api/notes'):
            self.handle_get_notes()
        elif path == '/api/info':
            self.handle_get_info()
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/api/notes':
            self.handle_save_note()
        else:
            self.send_error(404)

    def do_DELETE(self):
        """Handle DELETE requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path.startswith('/api/notes/'):
            self.handle_delete_note()
        else:
            self.send_error(404)

    def serve_svg_app(self):
        """Serve the main SVG PWA application"""
        try:
            with open('notepwa.svg', 'r', encoding='utf-8') as f:
                svg_content = f.read()
        except FileNotFoundError:
            # Fallback if SVG file doesn't exist
            svg_content = self.get_fallback_svg()

        self.send_response(200)
        self.send_header('Content-Type', 'image/svg+xml; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Access-Control-Allow-Origin', '*')
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

    def handle_delete_note(self):
        """Delete a note"""
        try:
            # Extract note ID from path
            path_parts = self.path.split('/')
            note_id = int(path_parts[-1])

            # Load existing notes
            if os.path.exists('notes.json'):
                with open('notes.json', 'r') as f:
                    notes = json.load(f)
            else:
                notes = []

            # Delete note if exists
            if 0 <= note_id < len(notes):
                notes.pop(note_id)

                # Update IDs for remaining notes
                for i, note in enumerate(notes):
                    note['id'] = i

                # Save updated notes
                with open('notes.json', 'w') as f:
                    json.dump(notes, f, indent=2)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'deleted'}).encode('utf-8'))
            else:
                self.send_error(404, 'Note not found')

        except (ValueError, IndexError):
            self.send_error(400, 'Invalid note ID')
        except Exception as e:
            self.send_error(500, str(e))

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
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'saved', 'id': note_data['id']}).encode('utf-8'))

        except Exception as e:
            self.send_error(500, str(e))

    def handle_get_info(self):
        """Get server info"""
        info = {
            "backend": "Python",
            "version": "1.0.0",
            "framework": "http.server"
        }

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(info).encode('utf-8'))

    def get_fallback_svg(self):
        def get_fallback_svg(self):
            """Generate a simple fallback SVG if main file is missing"""
            return '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 800 600">
  <rect width="100%" height="100%" fill="#f0f0f0"/>
  <text x="400" y="250" text-anchor="middle" font-family="Arial" font-size="24" fill="#333">
    NotePWA - Missing notepwa.svg file
  </text>
  <text x="400" y="300" text-anchor="middle" font-family="Arial" font-size="16" fill="#666">
    Please ensure notepwa.svg is in the same directory as this server
  </text>
  <text x="400" y="350" text-anchor="middle" font-family="Arial" font-size="14" fill="#999">
    Backend: Python HTTP Server
  </text>
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