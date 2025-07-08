# Dockerfile dla SVG Browser
FROM python:3.11-slim

# Metadane
LABEL maintainer="your.email@example.com"
LABEL description="SVG Browser - Lokalny serwer do przeglądania plików SVG"
LABEL version="0.1.0"

# Ustawienie katalogu roboczego
WORKDIR /app

# Instalacja zależności systemowych
RUN apt-get update && apt-get install -y \
    libxml2-dev \
    libxslt-dev \
    && rm -rf /var/lib/apt/lists/*

# Kopiowanie plików wymagań
COPY requirements.txt pyproject.toml ./

# Instalacja Poetry (opcjonalnie)
RUN pip install poetry

# Konfiguracja Poetry - bez tworzenia virtual env w kontenerze
RUN poetry config virtualenvs.create false

# Instalacja zależności
RUN poetry install --no-dev

# Alternatywnie można użyć pip:
# RUN pip install -r requirements.txt

# Kopiowanie kodu źródłowego
COPY svg_browser/ ./svg_browser/
COPY .env.example ./.env

# Tworzenie użytkownika nie-root dla bezpieczeństwa
RUN useradd --create-home --shell /bin/bash svguser
RUN chown -R svguser:svguser /app
USER svguser

# Eksponowanie portu
EXPOSE 5000

# Zmienne środowiskowe
ENV PORT=5000
ENV DEBUG=False
ENV PYTHONPATH=/app

# Sprawdzenie zdrowia kontenera
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Instalacja curl dla healthcheck
USER root
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
USER svguser

# Punkt wejścia
CMD ["python", "svg_browser/app.py"]

# Alternatywny punkt wejścia z gunicorn dla produkcji:
# RUN pip install gunicorn
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "svg_browser.app:app"]