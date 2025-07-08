#!/usr/bin/env python3
"""
SVG Browser - Lokalny serwer do przeglądania plików SVG
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from xml.etree import ElementTree as ET

from flask import Flask, render_template, send_file, jsonify, request
from dotenv import load_dotenv

# Ładowanie zmiennych środowiskowych
load_dotenv()

@dataclass
class SVGFile:
    """Klasa reprezentująca plik SVG z metadanymi"""
    path: str
    name: str
    size: int
    category: str
    has_javascript: bool = False
    has_metadata: bool = False
    metadata: Dict = None
    relative_path: str = ""

class SVGScanner:
    """Klasa do skanowania i kategoryzacji plików SVG"""
    
    def __init__(self):
        self.svg_files: List[SVGFile] = []
        
    def scan_paths(self, paths: List[str]) -> List[SVGFile]:
        """Skanuje podane ścieżki w poszukiwaniu plików SVG"""
        self.svg_files = []
        
        for path_str in paths:
            path = Path(path_str)
            if not path.exists():
                print(f"Ścieżka nie istnieje: {path}")
                continue
                
            print(f"Skanowanie: {path}")
            self._scan_directory(path)
            
        return self.svg_files
    
    def _scan_directory(self, directory: Path):
        """Rekursywnie skanuje katalog w poszukiwaniu plików SVG"""
        try:
            print(f"Skanowanie katalogu: {directory.absolute()}")
            if not directory.exists():
                print(f"  BŁĄD: Katalog nie istnieje: {directory}")
                return
                
            if not directory.is_dir():
                print(f"  BŁĄD: Ścieżka nie jest katalogiem: {directory}")
                return
                
            file_count = 0
            for file_path in directory.rglob("*.svg"):
                if file_path.is_file():
                    file_count += 1
                    if file_count % 100 == 0:
                        print(f"  Znaleziono {file_count} plików...")
                    try:
                        svg_file = self._analyze_svg_file(file_path)
                        if svg_file:
                            self.svg_files.append(svg_file)
                    except Exception as e:
                        print(f"  Błąd podczas analizy pliku {file_path}: {e}")
                        
            print(f"  Zakończono skanowanie. Znaleziono {file_count} plików SVG.")
            
        except PermissionError as e:
            print(f"  BŁĄD UPRAWNIEŃ: Brak uprawnień do odczytu: {directory}")
            print(f"  Szczegóły: {e}")
        except Exception as e:
            print(f"  NIESPODZIEWANY BŁĄD podczas skanowania {directory}:")
            import traceback
            traceback.print_exc()
    
    def _analyze_svg_file(self, file_path: Path) -> Optional[SVGFile]:
        """Analizuje plik SVG i określa jego kategorię"""
        # Skip macOS system files and directories
        if any(part.startswith('__MACOSX') or part.startswith('.') for part in file_path.parts):
            return None
            
        # Skip non-SVG files
        if file_path.suffix.lower() != '.svg':
            return None
            
        # Get absolute path and ensure it's normalized
        abs_path = str(file_path.absolute())
        file_size = file_path.stat().st_size
        
        # Try different encodings if UTF-8 fails
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
        content = None
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                break
            except UnicodeDecodeError:
                continue
                
        if content is None:
            print(f"  Nie można odczytać pliku {file_path} w żadnym z obsługiwanych kodowań")
            return None
        
        try:
            # Sprawdzenie czy plik zawiera JavaScript
            has_js = self._has_javascript(content)
            
            # Sprawdzenie metadanych
            metadata, has_metadata = self._extract_metadata(content)
            
            # Określenie kategorii
            if has_js:
                category = "pwa"
            elif has_metadata:
                category = "metadata"
            else:
                category = "graphic"
            
            return SVGFile(
                path=abs_path,
                name=file_path.name,
                size=file_size,
                category=category,
                has_javascript=has_js,
                has_metadata=has_metadata,
                metadata=metadata,
                relative_path=str(file_path.relative_to(Path.cwd()))
            )
            
        except Exception as e:
            print(f"Błąd podczas analizy pliku {file_path}: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _has_javascript(self, content: str) -> bool:
        """Sprawdza czy plik SVG zawiera JavaScript"""
        # Sprawdzenie tagów script
        if '<script' in content.lower():
            return True
            
        # Sprawdzenie atrybutów związanych z JavaScript
        js_patterns = [
            r'onclick\s*=',
            r'onload\s*=',
            r'onmouseover\s*=',
            r'javascript:',
            r'<script[^>]*>',
        ]
        
        for pattern in js_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
                
        return False
    
    def _extract_metadata(self, content: str) -> tuple:
        """Wyciąga metadane z pliku SVG"""
        metadata = {}
        has_metadata = False
        
        try:
            # Parsowanie XML
            root = ET.fromstring(content)
            
            # Sprawdzenie tytułu
            title_elem = root.find('.//{http://www.w3.org/2000/svg}title')
            if title_elem is not None and title_elem.text:
                metadata['title'] = title_elem.text.strip()
                has_metadata = True
            
            # Sprawdzenie opisu
            desc_elem = root.find('.//{http://www.w3.org/2000/svg}desc')
            if desc_elem is not None and desc_elem.text:
                metadata['description'] = desc_elem.text.strip()
                has_metadata = True
            
            # Sprawdzenie metadanych w korzeniu
            for attr_name in ['data-name', 'data-description', 'data-author', 'data-version']:
                if attr_name in root.attrib:
                    metadata[attr_name.replace('data-', '')] = root.attrib[attr_name]
                    has_metadata = True
            
            # Sprawdzenie elementu metadata
            metadata_elem = root.find('.//{http://www.w3.org/2000/svg}metadata')
            if metadata_elem is not None:
                has_metadata = True
                metadata['has_metadata_element'] = True
                
        except ET.ParseError:
            pass
            
        return metadata, has_metadata

# Inicjalizacja Flask
app = Flask(__name__)
scanner = SVGScanner()

@app.route('/')
def index():
    """Strona główna z przeglądarką plików SVG"""
    return render_template('index.html')

@app.route('/api/scan')
def api_scan():
    """API endpoint do skanowania plików SVG"""
    try:
        print("\n" + "="*50)
        print("Rozpoczęto skanowanie plików SVG")
        print("-"*50)
        
        # Pobieranie i walidacja ścieżek z .env
        scan_paths = os.getenv('SCAN_PATHS', '').strip()
        if not scan_paths:
            error_msg = 'Brak skonfigurowanych ścieżek w .env. Użyj SCAN_PATHS=ścieżka1,ścieżka2'
            print(f"BŁĄD: {error_msg}")
            return jsonify({
                'status': 'error',
                'error': error_msg
            }), 400
        
        # Przygotowanie ścieżek do skanowania
        paths = []
        for path in scan_paths.split(','):
            path = path.strip()
            if not path:
                continue
                
            expanded_path = os.path.expanduser(path)
            abs_path = os.path.abspath(expanded_path)
            
            print(f"\nPrzetwarzanie ścieżki: {path}")
            print(f"  Rozwinięta: {expanded_path}")
            print(f"  Bezwzględna: {abs_path}")
            print(f"  Istnieje: {os.path.exists(abs_path)}")
            
            if not os.path.exists(abs_path):
                print(f"  UWAGA: Ścieżka nie istnieje: {abs_path}")
            elif not os.path.isdir(abs_path):
                print(f"  UWAGA: Ścieżka nie jest katalogiem: {abs_path}")
            else:
                paths.append(abs_path)
        
        if not paths:
            error_msg = 'Brak prawidłowych ścieżek do skanowania. Sprawdź ustawienia SCAN_PATHS w .env'
            print(f"BŁĄD: {error_msg}")
            return jsonify({
                'status': 'error',
                'error': error_msg
            }), 400
        
        print(f"\nRozpoczęcie skanowania {len(paths)} katalogów...")
        
        # Skanowanie plików
        svg_files = scanner.scan_paths(paths)
        
        # Przygotowanie odpowiedzi
        categorized = {'graphic': [], 'pwa': [], 'metadata': []}
        
        for svg_file in svg_files:
            file_data = {
                'path': svg_file.path,
                'name': svg_file.name,
                'size': svg_file.size,
                'relative_path': svg_file.relative_path,
                'has_javascript': svg_file.has_javascript,
                'has_metadata': svg_file.has_metadata,
                'metadata': svg_file.metadata or {}
            }
            categorized[svg_file.category].append(file_data)
        
        total_files = len(svg_files)
        print(f"\nZakończono skanowanie. Znaleziono {total_files} plików SVG:")
        print(f"- Grafika: {len(categorized['graphic'])}")
        print(f"- Aplikacje PWA: {len(categorized['pwa'])}")
        print(f"- Z metadanymi: {len(categorized['metadata'])}")
        print("="*50 + "\n")
        
        return jsonify({
            'status': 'success',
            'total_files': total_files,
            'categories': categorized,
            'scan_paths': paths
        })
        
    except Exception as e:
        import traceback
        error_msg = f"Błąd podczas skanowania: {str(e)}"
        print(f"\n!!! BŁĄD KRYTYCZNY: {error_msg}")
        traceback.print_exc()
        print("="*50 + "\n")
        
        return jsonify({
            'status': 'error',
            'error': error_msg,
            'type': type(e).__name__,
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/file/<path:file_path>')
def api_get_file(file_path):
    """API endpoint do pobierania pliku SVG"""
    try:
        # Decode URL-encoded characters in the path
        import urllib.parse
        decoded_path = urllib.parse.unquote(file_path)
        
        # Ensure the path is absolute
        if not os.path.isabs(decoded_path):
            decoded_path = os.path.abspath(os.path.join('/', decoded_path))
        
        # Security check: prevent directory traversal
        normalized_path = os.path.normpath(decoded_path)
        if not normalized_path.startswith('/'):
            normalized_path = '/' + normalized_path
            
        # Log the file access attempt
        print(f"\n=== Debug: File Access ===")
        print(f"Original path: {file_path}")
        print(f"Decoded path: {decoded_path}")
        print(f"Normalized path: {normalized_path}")
        print(f"File exists: {os.path.exists(normalized_path)}")
        print(f"Is file: {os.path.isfile(normalized_path)}")
        
        # Check if file exists and is accessible
        if not os.path.exists(normalized_path):
            parent = os.path.dirname(normalized_path)
            print(f"Parent directory exists: {os.path.exists(parent)}")
            if os.path.exists(parent):
                try:
                    print(f"Contents of parent directory: {os.listdir(parent)}")
                except Exception as e:
                    print(f"Could not list parent directory: {e}")
            
            return jsonify({
                'error': 'File not found',
                'path': normalized_path,
                'exists': False,
                'is_file': False,
                'parent_exists': os.path.exists(parent)
            }), 404
        
        if not os.path.isfile(normalized_path):
            return jsonify({
                'error': 'Path is not a file',
                'path': normalized_path,
                'exists': True,
                'is_file': False,
                'is_dir': os.path.isdir(normalized_path)
            }), 400
        
        # Check file extension for security
        if not normalized_path.lower().endswith('.svg'):
            return jsonify({
                'error': 'Invalid file type. Only SVG files are allowed.',
                'path': normalized_path
            }), 400
            
        # Finally, serve the file
        return send_file(normalized_path, mimetype='image/svg+xml')
        
    except Exception as e:
        import traceback
        error_msg = f"Error accessing file: {str(e)}"
        print(f"\n!!! ERROR in api_get_file: {error_msg}")
        traceback.print_exc()
        
        return jsonify({
            'error': error_msg,
            'type': type(e).__name__,
            'path': file_path,
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/preview/<path:file_path>')
def api_preview_file(file_path):
    """API endpoint do podglądu zawartości pliku SVG"""
    try:
        # Decode URL-encoded characters in the path
        import urllib.parse
        decoded_path = urllib.parse.unquote(file_path)
        
        # Ensure the path is absolute
        if not os.path.isabs(decoded_path):
            decoded_path = os.path.abspath(os.path.join('/', decoded_path))
        
        # Security check: prevent directory traversal
        normalized_path = os.path.normpath(decoded_path)
        if not normalized_path.startswith('/'):
            normalized_path = '/' + normalized_path
            
        # Check if file exists and is accessible
        if not os.path.exists(normalized_path):
            return jsonify({
                'error': 'File not found',
                'path': normalized_path,
                'exists': False
            }), 404
            
        if not os.path.isfile(normalized_path):
            return jsonify({
                'error': 'Path is not a file',
                'path': normalized_path,
                'exists': True,
                'is_file': False
            }), 400
            
        # Check file extension for security
        if not normalized_path.lower().endswith('.svg'):
            return jsonify({
                'error': 'Invalid file type. Only SVG files are allowed.',
                'path': normalized_path
            }), 400
            
        # Read and return the file content
        with open(normalized_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        return jsonify({
            'status': 'success',
            'content': content,
            'path': normalized_path
        })
        
    except Exception as e:
        import traceback
        error_msg = f"Error reading file: {str(e)}"
        print(f"\n!!! ERROR in api_preview_file: {error_msg}")
        traceback.print_exc()
        
        return jsonify({
            'error': error_msg,
            'type': type(e).__name__,
            'path': file_path
        }), 500

def main():
    """Funkcja główna uruchamiająca serwer"""
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print(" Uruchamianie SVG Browser...")
    print(f" Serwer dostępny na: http://localhost:{port}")
    print("🚀 Uruchamianie SVG Browser...")
    print(f"📂 Serwer dostępny na: http://localhost:{port}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)

if __name__ == '__main__':
    main()