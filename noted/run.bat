@echo off
REM NotePWA Launcher Script for Windows
REM Automatically detects and runs the best available backend

echo 🎨 NotePWA Launcher
echo ==================
echo.

REM Check if notepwa.svg exists
if not exist "notepwa.svg" (
    echo ❌ Error: notepwa.svg not found!
    echo    Please ensure notepwa.svg is in the current directory.
    pause
    exit /b 1
)

REM Check if port 8000 is already in use
netstat -an | find "8000" | find "LISTENING" >nul
if %errorlevel% == 0 (
    echo ⚠️  Port 8000 is already in use!
    echo    NotePWA might already be running.
    echo    Opening browser...
    start http://localhost:8000
    pause
    exit /b 0
)

echo 🔍 Detecting available backends...
echo.

REM Option 1: Try Node.js
where node >nul 2>&1
if %errorlevel% == 0 (
    if exist "package.json" (
        echo ✅ Node.js detected

        REM Check if node_modules exists
        if not exist "node_modules" (
            echo 📦 Installing dependencies...
            npm install
            echo.
        )

        echo 🚀 Starting Node.js backend...
        echo    Framework: Express.js
        echo    URL: http://localhost:8000
        echo    Press Ctrl+C to stop
        echo.

        npm start
        pause
        exit /b 0
    )
)

REM Option 2: Try Python
where python >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Python detected
    echo 🚀 Starting Python backend...
    echo    Framework: http.server
    echo    URL: http://localhost:8000
    echo    Press Ctrl+C to stop
    echo.

    python note_server.py
    pause
    exit /b 0
)

REM Try python3 command
where python3 >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Python 3 detected
    echo 🚀 Starting Python backend...
    echo    Framework: http.server
    echo    URL: http://localhost:8000
    echo    Press Ctrl+C to stop
    echo.

    python3 note_server.py
    pause
    exit /b 0
)

REM No backend found
echo ❌ No suitable backend found!
echo.
echo Please install one of the following:
echo   • Node.js 14+ (recommended)
echo   • Python 3.7+
echo.
echo Then run this script again.
echo.
pause
exit /b 1