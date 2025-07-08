#!/usr/bin/env python3
"""
Skrypt do tworzenia struktury katalogów testowych z przykładowymi plikami SVG
"""

import os
from pathlib import Path

def create_test_structure():
    """Tworzy strukturę katalogów testowych"""
    
    base_dir = Path("test-svgs")
    
    # Katalogi do utworzenia
    directories = [
        "graphics",
        "pwa", 
        "metadata"
    ]
    
    print("🎨 Tworzenie struktury katalogów testowych...")
    
    # Tworzenie katalogów
    for directory in directories:
        dir_path = base_dir / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Utworzono katalog: {dir_path}")
    
    # Informacje o plikach
    print("\n📁 Struktura katalogów:")
    print(f"test-svgs/")
    print(f"├── graphics/          - Proste pliki SVG bez JS i metadanych")
    print(f"│   ├── simple-icon.svg")
    print(f"│   └── logo.svg")
    print(f"├── pwa/              - Interaktywne aplikacje SVG z JavaScript")
    print(f"│   ├── interactive-button.svg")
    print(f"│   └── calculator.svg")
    print(f"└── metadata/         - Pliki SVG z metadanymi")
    print(f"    ├── icon-with-meta.svg")
    print(f"    └── flowchart.svg")
    
    # Tworzenie pliku .env dla testów
    env_content = f"""# Testowa konfiguracja SVG Browser
# Używa lokalnych katalogów testowych

SCAN_PATHS={base_dir.absolute()}
PORT=5000
DEBUG=True
"""
    
    env_file = Path(".env.test")
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print(f"\n✅ Utworzono plik konfiguracyjny: {env_file}")
    print(f"\n🚀 Aby uruchomić serwer z testowymi plikami:")
    print(f"   1. cp .env.test .env")
    print(f"   2. make run")
    print(f"   lub: python svg_browser/app.py")

def create_readme_files():
    """Tworzy pliki README w katalogach testowych"""
    
    base_dir = Path("test-svgs")
    
    readmes = {
        "graphics/README.md": """# Graficzne pliki SVG

Ten katalog zawiera przykłady prostych plików SVG bez JavaScript i metadanych.

## Pliki:
- `simple-icon.svg` - Prosta ikona z checkmarkiem
- `logo.svg` - Logo firmy z gradientem

Te pliki zostaną skategoryzowane jako "Graficzne".
""",
        "pwa/README.md": """# PWA/JS - Interaktywne aplikacje SVG

Ten katalog zawiera pliki SVG z kodem JavaScript - interaktywne aplikacje.

## Pliki:
- `interactive-button.svg` - Przycisk z animacją i licznikiem kliknięć
- `calculator.svg` - Pełnofunkcjonalny kalkulator w SVG

Te pliki zostaną skategoryzowane jako "PWA/JS".
""",
        "metadata/README.md": """# Pliki SVG z metadanymi

Ten katalog zawiera pliki SVG z metadanymi (tytuł, opis, autor, itp.).

## Pliki:
- `icon-with-meta.svg` - Ikona z tytułem, opisem i metadanymi RDF
- `flowchart.svg` - Diagram z pełnymi metadanymi

Te pliki zostaną skategoryzowane jako "Metadane".
"""
    }
    
    for file_path, content in readmes.items():
        full_path = base_dir / file_path
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Utworzono: {full_path}")

if __name__ == "__main__":
    create_test_structure()
    create_readme_files()
    print("\n🎉 Struktura testowa gotowa!")
