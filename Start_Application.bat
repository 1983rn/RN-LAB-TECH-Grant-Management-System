@echo off
TITLE Grant Management System
echo Starting Grant Management System...

REM Check for virtual environment and activate if present
if exist .venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
) else (
    echo Virtual environment not found, using system Python...
)

REM Check and install openpyxl if missing
echo Checking dependencies...
python -c "import openpyxl" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Installing openpyxl for Excel export feature...
    pip install openpyxl==3.1.2
    echo.
)

REM Initialize authentication system if database doesn't exist
if not exist data\grant_management.db (
    echo.
    echo ========================================
    echo FIRST TIME SETUP - Initializing System
    echo ========================================
    python setup_auth.py
    echo.
    echo Press any key to continue...
    pause >nul
) else (
    echo Database exists, verifying developer account...
    python -c "from database import get_db; conn = get_db().__enter__(); cursor = conn.cursor(); cursor.execute('SELECT id FROM schools WHERE username = ?', ('juniornsambe@yahoo.com',)); result = cursor.fetchone(); conn.__exit__(None, None, None); exit(0 if result else 1)" 2>nul
    if %ERRORLEVEL% NEQ 0 (
        echo Developer account missing, fixing...
        python fix_dev_login.py
    )
    echo Running database migrations...
    python add_school_name_column.py 2>nul
    echo Ensuring template-based budget structure...
    python migrate_template_row_id.py 2>nul
    echo Optimizing database for concurrent access...
    python enable_wal.py 2>nul
)

REM Run the application
echo.
echo ========================================
echo Starting Application...
echo Access at: http://localhost:5176
echo ========================================
echo.
echo LOGIN CREDENTIALS:
echo   School: NANJATICDSS / 1994
echo   Developer: Type 'devaccess' on login
echo ========================================
echo.
python app.py

REM Pause if the application crashes so user can see the error
if %ERRORLEVEL% NEQ 0 (
    echo Application exited with error code %ERRORLEVEL%
    pause
)
