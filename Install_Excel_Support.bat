@echo off
TITLE Install Excel Export Dependency
echo ========================================
echo Installing openpyxl for Excel Export
echo ========================================
echo.

REM Check for virtual environment and activate if present
if exist .venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
    echo.
    echo Installing openpyxl in virtual environment...
    pip install openpyxl==3.1.2
) else (
    echo Virtual environment not found, installing to system Python...
    echo.
    pip install openpyxl==3.1.2
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo You can now use the "Download Excel" feature.
echo Please restart the application for changes to take effect.
echo.
pause
