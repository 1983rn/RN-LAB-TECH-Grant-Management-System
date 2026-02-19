@echo off
TITLE Grant Management System - Multi-Tenant Setup
echo ========================================
echo Grant Management System
echo Multi-Tenant Architecture Setup
echo ========================================
echo.

REM Check for virtual environment
if exist .venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
) else (
    echo Virtual environment not found, using system Python...
)

REM Check if database exists
if not exist data\grant_management.db (
    echo.
    echo [FIRST TIME SETUP]
    echo Running database migration...
    echo.
    python migrate.py
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo ERROR: Migration failed!
        pause
        exit /b 1
    )
    echo.
    echo ========================================
    echo SETUP COMPLETE!
    echo ========================================
    echo.
    echo Default School Credentials:
    echo   Username: admin
    echo   Password: admin123
    echo.
    echo Developer Access:
    echo   1. Type 'devaccess' on login screen
    echo   2. Username: juniornsambe@yahoo.com
    echo   3. Password: blessings19831983/
    echo.
    echo ========================================
    echo.
    pause
)

REM Start the application
echo Starting application...
echo Access at: http://localhost:5176
echo.
python app.py

REM Pause if error
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Application exited with error code %ERRORLEVEL%
    pause
)
