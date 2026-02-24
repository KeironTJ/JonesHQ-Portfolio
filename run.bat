@echo off
setlocal

echo.
echo  ========================================
echo   JonesHQ Portfolio - Dev Environment
echo  ========================================
echo.

REM ── Virtual environment ──────────────────────────────────────────────────────
if not exist "venv\" (
    echo [1/3] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Could not create venv. Is Python 3.10+ installed and on PATH?
        pause
        exit /b 1
    )
) else (
    echo [1/3] Virtual environment found.
)

call venv\Scripts\activate.bat

REM ── Dependencies ─────────────────────────────────────────────────────────────
echo [2/3] Installing / syncing dependencies...
pip install -r requirements.txt -q
if errorlevel 1 (
    echo ERROR: pip install failed.
    pause
    exit /b 1
)

REM ── .env ─────────────────────────────────────────────────────────────────────
if not exist ".env" (
    copy /y ".env.example" ".env" > nul
    echo.
    echo  NOTE: .env was created from .env.example.
    echo        Edit it and set SECRET_KEY before using in production.
    echo.
)

REM ── Flask config ─────────────────────────────────────────────────────────────
set FLASK_APP=run.py
set FLASK_DEBUG=1
set FLASK_CONFIG=development

echo [3/3] Ready.
echo.
echo  Useful commands (run in this terminal after activation):
echo    flask init-db              -- create database tables
echo    flask create-admin ^<user^> ^<pass^>  -- create the admin account
echo.
echo  Starting Flask dev server at http://127.0.0.1:5000
echo  Press Ctrl+C to stop.
echo.

flask run

pause
