#!/usr/bin/env python3
"""
Skrypt naprawczy dla problemów z instalacją SVG Browser
"""

import sys
import subprocess
import os
from pathlib import Path

def clear_poetry_cache():
    """Czyści cache Poetry"""
    print("🧹 Czyszczenie cache Poetry...")
    try:
        subprocess.run(['poetry', 'cache', 'clear', '--all', 'pypi'], 
                      capture_output=True, check=False)
        print("✅ Cache Poetry wyczyszczony")
    except FileNotFoundError:
        print("⚠️  Poetry nie jest zainstalowane")

def reset_virtualenv():
    """Resetuje środowisko wirtualne Poetry"""
    print("🔄 Resetowanie środowiska wirtualnego...")
    try:
        # Usuń obecne środowisko
        result = subprocess.run(['poetry', 'env', 'info', '--path'], 
                              capture_output=True, text=True, check=False)
        if result.returncode == 0:
            env_path = result.stdout.strip()
            subprocess.run(['poetry', 'env', 'remove', 'python'], 
                          capture_output=True, check=False)
            print(f"✅ Usunięto środowisko: {env_path}")
        
        # Stwórz nowe
        subprocess.run(['poetry', 'env', 'use', 'python'], 
                      capture_output=True, check=False)
        print("✅ Stworzone nowe środowisko")
        
    except FileNotFoundError:
        print("⚠️  Poetry nie jest zainstalowane")

def check_python_version():
    """Sprawdza wersję Pythona"""
    print("🐍 Sprawdzanie wersji Pythona...")
    version = sys.version_info
    print(f"Obecna wersja: {version.major}.{version.minor}.{version.micro}")
    
    if version < (3, 8, 1):
        print("❌ BŁĄD: Wymagany Python 3.8.1 lub nowszy")
        print("💡 Rozwiązania:")
        print("   1. Zainstaluj nowszego Pythona z https://python.org")
        print("   2. Użyj pyenv do zarządzania wersjami:")
        print("      pyenv install 3.11.0")
        print("      pyenv local 3.11.0")
        return False
    else:
        print("✅ Wersja Pythona jest kompatybilna")
        return True

def try_pip_install():
    """Próbuje instalacji przez pip jako alternatywa"""
    print("🔄 Próba instalacji przez pip...")
    try:
        # Sprawdź czy requirements.txt istnieje
        if not Path('requirements.txt').exists():
            print("❌ Brak pliku requirements.txt")
            return False
        
        # Zainstaluj przez pip
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True)
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-e', '.'], 
                      check=True)
        print("✅ Instalacja przez pip zakończona")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Błąd instalacji pip: {e}")
        return False
    except FileNotFoundError:
        print("❌ pip nie jest dostępny")
        return False

def fix_pyproject_toml():
    """Naprawia wymagania Pythona w pyproject.toml"""
    print("🔧 Sprawdzanie pyproject.toml...")
    
    pyproject_path = Path('pyproject.toml')
    if not pyproject_path.exists():
        print("❌ Brak pliku pyproject.toml")
        return False
    
    try:
        content = pyproject_path.read_text(encoding='utf-8')
        
        # Sprawdź czy trzeba naprawić
        if 'python = "^3.8"' in content:
            print("🔧 Naprawianie wymagań Pythona...")
            content = content.replace('python = "^3.8"', 'python = "^3.8.1"')
            pyproject_path.write_text(content, encoding='utf-8')
            print("✅ pyproject.toml naprawiony")
            return True
        else:
            print("✅ pyproject.toml już ma poprawne wymagania")
            return True
            
    except Exception as e:
        print(f"❌ Błąd naprawiania pyproject.toml: {e}")
        return False

def main():
    """Główna funkcja naprawcza"""
    print("🔧 SVG Browser - Naprawa instalacji")
    print("=" * 40)
    
    # Sprawdź Pythona
    if not check_python_version():
        return
    
    # Napraw pyproject.toml
    fix_pyproject_toml()
    
    print("\n🔄 Opcje naprawy:")
    print("1. Resetowanie Poetry (zalecane)")
    print("2. Instalacja przez pip")
    print("3. Tylko czyszczenie cache")
    
    choice = input("\nWybierz opcję (1-3): ").strip()
    
    if choice == "1":
        clear_poetry_cache()
        reset_virtualenv()
        print("\n🚀 Spróbuj teraz: poetry install")
        
    elif choice == "2":
        if try_pip_install():
            print("\n🚀 Instalacja zakończona. Uruchom: python svg_browser/app.py")
        else:
            print("\n❌ Instalacja przez pip nie powiodła się")
            
    elif choice == "3":
        clear_poetry_cache()
        print("\n🚀 Spróbuj teraz: poetry install")
        
    else:
        print("❌ Nieprawidłowy wybór")
    
    print("\n💡 Jeśli nadal masz problemy:")
    print("   - Sprawdź czy masz Python 3.8.1+")
    print("   - Użyj: python start.py (automatyczna diagnoza)")
    print("   - Zobacz INSTALL.md dla więcej opcji")

if __name__ == '__main__':
    main()
