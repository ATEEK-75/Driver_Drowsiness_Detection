@echo off
title Driver Drowsiness Detection
cd /d "%~dp0"

if not exist .venv (
    echo Creating virtual environment...
    py -3.11 -m venv .venv 2>nul
    if errorlevel 1 (
        echo Python 3.11 not found via 'py -3.11', trying default Python...
        py -m venv .venv 2>nul
    )
    if errorlevel 1 (
        python -m venv .venv 2>nul
    )
    if not exist .venv (
        echo [ERROR] Could not create virtual environment.
        echo Please ensure Python is installed and added to PATH.
        pause
        exit /b 1
    )
    echo Virtual environment created successfully.
)

call .venv\Scripts\activate
echo Checking dependencies...
python -m pip install -r requirements.txt
echo Starting Driver Drowsiness Detection...
python app.py
pause
