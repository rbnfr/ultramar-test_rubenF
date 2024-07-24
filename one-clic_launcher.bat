@echo off
setlocal enabledelayedexpansion

set VENV_NAME=.venv

set SCRIPT_DIR=%~dp0
set PROJECT_PATH=%SCRIPT_DIR%


REM Check if virtual environment exists
if not exist "%VENV_NAME%\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv %VENV_NAME%
    
    call %VENV_NAME%\Scripts\activate.bat
    
    if exist "%PROJECT_PATH%\requirements.txt" (
        echo Installing requirements from requirements.txt...
        pip install -r "%PROJECT_PATH%\requirements.txt"
    ) else (
        echo requirements.txt not found. Skipping requirements installation.
    )
) else (
    call %VENV_NAME%\Scripts\activate.bat
)

cd /d %PROJECT_PATH%

start "" python manage.py makemigrations
start "" python manage.py migrate
start "" python manage.py runserver
timeout /t 2 /nobreak

start http://127.0.0.1:8000

echo Django server is running. Press Ctrl+C to stop the server.
pause
