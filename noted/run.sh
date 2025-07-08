#!/bin/bash

# NotePWA Launcher Script
# Automatically detects and runs the best available backend

echo "🎨 NotePWA Launcher"
echo "=================="
echo ""

# Check if notepwa.svg exists
if [ ! -f "notepwa.svg" ]; then
    echo "❌ Error: notepwa.svg not found!"
    echo "   Please ensure notepwa.svg is in the current directory."
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if port is available
port_available() {
    ! lsof -i:8000 >/dev/null 2>&1
}

# Check if port 8000 is already in use
if ! port_available; then
    echo "⚠️  Port 8000 is already in use!"
    echo "   NotePWA might already be running."
    echo "   Opening browser..."

    # Try to open browser
    if command_exists open; then
        open http://localhost:8000
    elif command_exists xdg-open; then
        xdg-open http://localhost:8000
    elif command_exists start; then
        start http://localhost:8000
    else
        echo "   Go to: http://localhost:8000"
    fi
    exit 0
fi

echo "🔍 Detecting available backends..."
echo ""

# Option 1: Try Node.js
if command_exists node && [ -f "package.json" ]; then
    echo "✅ Node.js detected"

    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        echo "📦 Installing dependencies..."
        npm install
        echo ""
    fi

    echo "🚀 Starting Node.js backend..."
    echo "   Framework: Express.js"
    echo "   URL: http://localhost:8000"
    echo "   Press Ctrl+C to stop"
    echo ""

    npm start
    exit 0
fi

# Option 2: Try Python
if command_exists python3; then
    echo "✅ Python 3 detected"
    echo "🚀 Starting Python backend..."
    echo "   Framework: http.server"
    echo "   URL: http://localhost:8000"
    echo "   Press Ctrl+C to stop"
    echo ""

    python3 note_server.py
    exit 0
elif command_exists python; then
    echo "✅ Python detected"
    echo "🚀 Starting Python backend..."
    echo "   Framework: http.server"
    echo "   URL: http://localhost:8000"
    echo "   Press Ctrl+C to stop"
    echo ""

    python note_server.py
    exit 0
fi

# No backend found
echo "❌ No suitable backend found!"
echo ""
echo "Please install one of the following:"
echo "  • Node.js 14+ (recommended)"
echo "  • Python 3.7+"
echo ""
echo "Then run this script again."
exit 1