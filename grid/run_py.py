#!/usr/bin/env python3
"""
Alternatywny punkt wejścia dla SVG Browser
Użycie: python run.py
"""

import sys
import os

# Dodanie ścieżki do modułu
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import i uruchomienie aplikacji
from svg_browser.app import main

if __name__ == '__main__':
    main()