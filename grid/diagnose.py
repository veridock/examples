#!/usr/bin/env python3
"""
Narzędzie diagnostyczne dla SVG Browser
Sprawdza wszystkie aspekty instalacji i konfiguracji
"""

import sys
import os
import subprocess
from pathlib import Path
import platform

def print_header(title):
    """Wyświetla nagłówek sekcji"""
    print(f"\n{'='*50}")
    print(f"🔍 {title}")
    print('='*50)

def check_system():
    """Sprawdza informacje o systemie"""
    print_header("INFORMACJE O SYSTEMIE")
    
    print(f"System: {platform.system()} {platform.release()}")
    print(f"Architektura: {platform.machine()}")
    print(f"Python: {sys.version}")
    print(f"Python executable: {sys.executable}")
    
    # Sprawdź pip
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"Pip: {result.stdout.strip()}")
    except:
        print("❌ Pip nie jest dostępny")
    
    # Sprawdź Poetry
    try:
        result = subprocess.run(['poetry', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"Poetry: {result.stdout.strip()}")
    except:
        print("⚠️  Poetry nie jest zainstalowane")

def check_project_files():
    """Sprawdza pliki projektu"""
    print_header("PLIKI PROJEKTU")
    
    required_files = [
        'pyproject.toml',
        'requirements.txt', 
        'svg_browser/__init__.py',
        'svg_browser/app.py',
        'svg_browser/templates/index.html'
    ]
    
    optional_files = [
        '.env',
        '.env.example',
        'Makefile',
        'README.md'
    ]
    
    print("Wymagane pliki:")
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} (BRAK)")
    
    print("\nOpcjonalne pliki:")
    for file_path in optional_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"⚠️  {file_path}")

def check_dependencies():
    """Sprawdza zależności"""
    print_header("ZALEŻNOŚCI")
    
    required_packages = {
        'flask': 'Flask web framework',
        'dotenv': 'python-dotenv (zmienne środowiskowe)', 
        'lxml': 'XML parser'
    }
    
    for package, description in required_packages.items():
        try:
            if package == 'dotenv':
                import dotenv
                version = getattr(dotenv, '__version__', 'unknown')
            else:
                module = __import__(package)
                version = getattr(module, '__version__', 'unknown')
            
            print(f"✅ {package} ({version}) - {description}")
            
        except ImportError:
            print(f"❌ {package} - {description} (BRAK)")

def check_configuration():
    """Sprawdza konfigurację"""
    print_header("KONFIGURACJA")
    
    # Sprawdź .env
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ Brak pliku .env")
        if Path('.env.example').exists():
            print("💡 Można skopiować: cp .env.example .env")
        return
    
    print("✅ Plik .env istnieje")
    
    # Sprawdź zawartość .env
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        scan_paths = os.getenv('SCAN_PATHS', '')
        port = os.getenv('PORT', '5000')
        debug = os.getenv('DEBUG', 'False')
        
        print(f"PORT: {port}")
        print(f"DEBUG: {debug}")
        
        if not scan_paths:
            print("❌ Brak SCAN_PATHS w .env")
            return
        
        print(f"SCAN_PATHS: {scan_paths}")
        
        # Sprawdź ścieżki
        paths = [p.strip() for p in scan_paths.split(',') if p.strip()]
        print("\nStwierdzenie ścieżek:")
        valid_paths = 0
        for path in paths:
            path_obj = Path(path)
            if path_obj.exists():
                if path_obj.is_dir():
                    svg_count = len(list(path_obj.rglob('*.svg')))
                    print(f"✅ {path} ({svg_count} plików SVG)")
                    valid_paths += 1
                else:
                    print(f"⚠️  {path} (nie jest katalogiem)")
            else:
                print(f"❌ {path} (nie istnieje)")
        
        if valid_paths == 0:
            print("❌ Żadna ścieżka nie zawiera plików SVG")
        else:
            print(f"✅ {valid_paths} z {len(paths)} ścieżek jest prawidłowych")
            
    except ImportError:
        print("❌ python-dotenv nie jest zainstalowane")
    except Exception as e:
        print(f"❌ Błąd sprawdzania konfiguracji: {e}")

def check_test_server():
    """Sprawdza czy serwer może być uruchomiony"""
    print_header("TEST SERWERA")
    
    try:
        # Próba importu
        sys.path.insert(0, '.')
        from svg_browser.app import app
        print("✅ Import modułu app udany")
        
        # Sprawdź czy Flask może być uruchomiony
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Serwer Flask działa poprawnie")
            else:
                print(f"⚠️  Serwer odpowiada z kodem: {response.status_code}")
                
    except ImportError as e:
        print(f"❌ Błąd importu: {e}")
    except Exception as e:
        print(f"❌ Błąd testu serwera: {e}")

def suggest_solutions():
    """Proponuje rozwiązania problemów"""
    print_header("SUGEROWANE ROZWIĄZANIA")
    
    print("🔧 Jeśli masz problemy z instalacją:")
    print("   python fix_install.py")
    print("")
    print("🚀 Alternatywne sposoby uruchomienia:")
    print("   python quick_start.py    # Automatyczna instalacja pip")
    print("   python start.py          # Interaktywny starter")
    print("   make fix                 # Naprawa przez Makefile")
    print("")
    print("📦 Instalacja zależności:")
    print("   poetry install           # Przez Poetry")
    print("   pip install -r requirements.txt  # Przez pip")
    print("")
    print("⚙️  Konfiguracja:")
    print("   cp .env.example .env     # Skopiuj przykład")
    print("   python create_test_structure.py  # Stwórz pliki testowe")

def main():
    """Główna funkcja diagnostyczna"""
    print("🩺 SVG Browser - Diagnostyka")
    print(f"Katalog: {Path.cwd()}")
    
    check_system()
    check_project_files()
    check_dependencies()
    check_configuration()
    check_test_server()
    suggest_solutions()
    
    print_header("PODSUMOWANIE")
    print("Sprawdź komunikaty ❌ powyżej i użyj sugerowanych rozwiązań.")
    print("Jeśli wszystko jest ✅ - serwer powinien działać poprawnie!")

if __name__ == '__main__':
    main()
