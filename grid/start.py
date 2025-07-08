#!/usr/bin/env python3
"""
Prosty skrypt startowy dla SVG Browser
Automatycznie sprawdza konfigurację i uruchamia serwer
"""

import os
import sys
from pathlib import Path

def check_requirements():
    """Sprawdza czy wszystkie wymagania są spełnione"""
    print("🔍 Sprawdzanie wymagań...")
    
    # Sprawdzenie Python
    if sys.version_info < (3, 8):
        print("❌ Wymagany Python 3.8 lub nowszy")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    
    # Sprawdzenie modułów
    required_modules = ['flask', 'dotenv', 'lxml']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            missing_modules.append(module)
            print(f"❌ {module}")
    
    if missing_modules:
        print(f"\n⚠️  Brakujące moduły: {', '.join(missing_modules)}")
        print("Instalacja:")
        print("  Poetry: poetry install")
        print("  Pip:    pip install -r requirements.txt")
        return False
    
    return True

def check_config():
    """Sprawdza konfigurację"""
    print("\n📂 Sprawdzanie konfiguracji...")
    
    # Sprawdzenie pliku .env
    if not Path('.env').exists():
        print("❌ Brak pliku .env")
        
        if Path('.env.example').exists():
            print("💡 Znaleziono .env.example")
            response = input("Skopiować .env.example jako .env? (t/n): ")
            if response.lower() in ['t', 'tak', 'y', 'yes']:
                import shutil
                shutil.copy('.env.example', '.env')
                print("✅ Skopiowano .env.example -> .env")
            else:
                print("⚠️  Musisz stworzyć plik .env z konfiguracją")
                return False
        else:
            print("⚠️  Brak pliku .env.example - stwórz plik .env ręcznie")
            return False
    
    # Sprawdzenie ścieżek
    from dotenv import load_dotenv
    load_dotenv()
    
    scan_paths = os.getenv('SCAN_PATHS', '')
    if not scan_paths:
        print("❌ Brak skonfigurowanych ścieżek SCAN_PATHS w .env")
        print("💡 Dodaj ścieżki do skanowania, np.:")
        print("   SCAN_PATHS=/path/to/svg/files,/another/path")
        return False
    
    print(f"✅ Plik .env istnieje")
    
    # Sprawdzenie czy ścieżki istnieją
    paths = [p.strip() for p in scan_paths.split(',') if p.strip()]
    valid_paths = []
    
    for path in paths:
        if Path(path).exists():
            print(f"✅ {path}")
            valid_paths.append(path)
        else:
            print(f"⚠️  {path} (nie istnieje)")
    
    if not valid_paths:
        print("❌ Żadna ze skonfigurowanych ścieżek nie istnieje")
        return False
    
    return True

def create_test_files():
    """Oferuje stworzenie plików testowych"""
    if not Path('test-svgs').exists():
        print("\n🧪 Nie znaleziono katalogu testowego")
        response = input("Stworzyć pliki testowe? (t/n): ")
        if response.lower() in ['t', 'tak', 'y', 'yes']:
            try:
                exec(open('create_test_structure.py').read())
                return True
            except FileNotFoundError:
                print("❌ Brak pliku create_test_structure.py")
            except Exception as e:
                print(f"❌ Błąd tworzenia plików testowych: {e}")
    return False

def start_server():
    """Uruchamia serwer"""
    print("\n🚀 Uruchamianie SVG Browser...")
    
    try:
        # Import i uruchomienie
        from svg_browser.app import main
        main()
    except ImportError:
        print("❌ Błąd importu - sprawdź instalację")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Zamykanie serwera...")
    except Exception as e:
        print(f"❌ Błąd: {e}")
        sys.exit(1)

def main():
    """Główna funkcja startowa"""
    print("🎨 SVG Browser - Starter")
    print("=" * 40)
    
    # Sprawdzenia
    if not check_requirements():
        sys.exit(1)
    
    if not check_config():
        sys.exit(1)
    
    # Opcjonalne - pliki testowe
    if create_test_files():
        print("✅ Pliki testowe utworzone")
    
    # Uruchomienie
    start_server()

if __name__ == '__main__':
    main()
