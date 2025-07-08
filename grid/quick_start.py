#!/usr/bin/env python3
"""
Szybki start bez Poetry - automatycznie instaluje zależności przez pip
"""

import sys
import subprocess
import os
from pathlib import Path

def install_requirements():
    """Instaluje wymagania przez pip"""
    print("📦 Instalowanie zależności...")
    
    required_packages = [
        'flask>=2.3.0',
        'python-dotenv>=1.0.0', 
        'lxml>=4.9.0'
    ]
    
    for package in required_packages:
        try:
            print(f"Instalowanie {package}...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                          check=True, capture_output=True)
            print(f"✅ {package}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Błąd instalacji {package}: {e}")
            return False
    
    return True

def check_and_create_env():
    """Sprawdza i tworzy plik .env"""
    if not Path('.env').exists():
        if Path('.env.example').exists():
            print("📋 Kopiowanie .env.example -> .env")
            import shutil
            shutil.copy('.env.example', '.env')
        else:
            print("📋 Tworzenie podstawowego .env")
            with open('.env', 'w') as f:
                f.write("SCAN_PATHS=./test-svgs\nPORT=5000\nDEBUG=True\n")
    
    print("✅ Plik .env gotowy")

def create_test_files():
    """Tworzy podstawowe pliki testowe"""
    test_dir = Path("test-svgs/graphics")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    # Prosty plik SVG testowy
    simple_svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="40" fill="#3498db"/>
  <text x="50" y="55" text-anchor="middle" fill="white" font-size="16">SVG</text>
</svg>'''
    
    test_file = test_dir / "test-icon.svg"
    if not test_file.exists():
        test_file.write_text(simple_svg, encoding='utf-8')
        print(f"✅ Utworzono plik testowy: {test_file}")

def main():
    """Główna funkcja quick start"""
    print("🚀 SVG Browser - Quick Start")
    print("=" * 30)
    
    # Sprawdź Pythona
    if sys.version_info < (3, 8, 1):
        print("❌ Wymagany Python 3.8.1+")
        print(f"   Obecna wersja: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        sys.exit(1)
    
    print("✅ Python OK")
    
    # Instaluj zależności
    if not install_requirements():
        print("❌ Błąd instalacji zależności")
        sys.exit(1)
    
    # Konfiguracja
    check_and_create_env()
    create_test_files()
    
    print("\n🎉 Instalacja zakończona!")
    print("\n🚀 Uruchamianie serwera...")
    
    # Import i uruchomienie
    try:
        sys.path.insert(0, '.')
        from svg_browser.app import main as app_main
        app_main()
    except ImportError as e:
        print(f"❌ Błąd importu: {e}")
        print("💡 Spróbuj: python svg_browser/app.py")
    except KeyboardInterrupt:
        print("\n👋 Zamknięto serwer")

if __name__ == '__main__':
    main()
