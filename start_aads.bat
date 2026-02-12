@echo off
REM AADS Series Manager - Quick Start Launcher for Windows
REM Double-click this file to run the program

title AADS Series Manager

echo.
echo ========================================
echo   AADS SERIES MANAGER
echo   Atlantic Armwrestling Development
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.7 or higher from python.org
    echo.
    pause
    exit /b 1
)

REM Check if database exists
if not exist "aads_series.db" (
    echo Database not found. Initializing...
    echo.
    python initialize_data.py
    if errorlevel 1 (
        echo.
        echo ERROR: Database initialization failed
        pause
        exit /b 1
    )
    echo.
    echo Database initialized successfully!
    echo.
    pause
)

REM Run the manager
echo Starting AADS Manager...
echo.
python aads_manager.py

if errorlevel 1 (
    echo.
    echo ERROR: Program exited with an error
    pause
)
