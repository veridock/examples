"""
Konfiguracja dla SVG Browser
"""

import os
from typing import List
from dotenv import load_dotenv

# Ładowanie zmiennych środowiskowych
load_dotenv()

class Config:
    """Klasa konfiguracji aplikacji"""
    
    # Podstawowe ustawienia serwera
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    HOST = os.getenv('HOST', '0.0.0.0')
    
    # Ścieżki do skanowania
    SCAN_PATHS_RAW = os.getenv('SCAN_PATHS', '')
    
    @property
    def scan_paths(self) -> List[str]:
        """Zwraca listę ścieżek do skanowania"""
        if not self.SCAN_PATHS_RAW:
            return []
        return [path.strip() for path in self.SCAN_PATHS_RAW.split(',') if path.strip()]
    
    # Ustawienia skanowania
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 10 * 1024 * 1024))  # 10MB
    SUPPORTED_EXTENSIONS = ['.svg']
    
    # Ustawienia kategoryzacji
    JS_PATTERNS = [
        r'<script[^>]*>',
        r'onclick\s*=',
        r'onload\s*=',
        r'onmouseover\s*=',
        r'onmouseout\s*=',
        r'onchange\s*=',
        r'javascript:',
    ]
    
    METADATA_ELEMENTS = [
        'title',
        'desc', 
        'metadata'
    ]
    
    METADATA_ATTRIBUTES = [
        'data-name',
        'data-description', 
        'data-author',
        'data-version',
        'data-license'
    ]
    
    # Ustawienia cache (opcjonalne - dla przyszłych wersji)
    ENABLE_CACHE = os.getenv('ENABLE_CACHE', 'False').lower() == 'true'
    CACHE_TTL = int(os.getenv('CACHE_TTL', 3600))  # 1 godzina
    
    # Ustawienia logowania
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Bezpieczeństwo
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    
    # Ustawienia interfejsu
    ITEMS_PER_PAGE = int(os.getenv('ITEMS_PER_PAGE', 50))
    PREVIEW_SIZE = os.getenv('PREVIEW_SIZE', '150px')
    
    @classmethod
    def validate(cls) -> List[str]:
        """Walidacja konfiguracji, zwraca listę błędów"""
        errors = []
        
        # Sprawdzenie ścieżek
        config = cls()
        if not config.scan_paths:
            errors.append("Brak skonfigurowanych ścieżek w SCAN_PATHS")
        
        # Sprawdzenie czy ścieżki istnieją
        for path in config.scan_paths:
            if not os.path.exists(path):
                errors.append(f"Ścieżka nie istnieje: {path}")
        
        # Sprawdzenie portu
        if not (1 <= config.PORT <= 65535):
            errors.append(f"Nieprawidłowy port: {config.PORT}")
        
        return errors
    
    def __repr__(self):
        return f"<Config(port={self.PORT}, debug={self.DEBUG}, paths={len(self.scan_paths)})>"

class DevelopmentConfig(Config):
    """Konfiguracja dla środowiska deweloperskiego"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Konfiguracja dla środowiska produkcyjnego"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    HOST = '0.0.0.0'

class TestingConfig(Config):
    """Konfiguracja dla testów"""
    DEBUG = True
    TESTING = True
    SCAN_PATHS_RAW = './test-svgs'

# Mapowanie nazw konfiguracji
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': Config
}

def get_config(config_name: str = None) -> Config:
    """
    Zwraca konfigurację na podstawie nazwy środowiska
    
    Args:
        config_name: Nazwa konfiguracji (development, production, testing)
    
    Returns:
        Instancja klasy konfiguracji
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
    
    config_class = config_map.get(config_name, Config)
    return config_class()