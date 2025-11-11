@echo off
echo ========================================
echo DevOpsHub Setup (Windows)
echo ========================================
echo.

echo Checking for existing virtual environment...
if exist .venv (
    echo Found existing .venv folder. Please delete it first.
    echo Run: rmdir /s .venv
    echo Then run setup.bat again.
    pause
    exit /b 1
)

echo [1/3] Creating virtual environment...
python -m venv .venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    echo Please ensure Python 3.8+ is installed
    pause
    exit /b 1
)

echo [2/3] Activating virtual environment...
call .venv\Scripts\activate.bat

echo [3/3] Installing dependencies (this may take a few minutes)...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To run DevOpsHub:
echo   1. Activate virtual environment: .venv\Scripts\activate
echo   2. Run the app: streamlit run app.py
echo.
pause
