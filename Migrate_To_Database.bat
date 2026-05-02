@echo off
TITLE Migrate to Multi-Tenant Database
echo ========================================
echo MIGRATING FROM JSON TO DATABASE
echo ========================================
echo.
echo This will migrate all JSON data to the multi-tenant database.
echo Your JSON files will be backed up but not deleted.
echo.
pause

python migrate_to_database.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo MIGRATION SUCCESSFUL!
    echo ========================================
    echo.
    echo Next steps:
    echo 1. Restart the application
    echo 2. Test all functionality
    echo 3. If everything works, you can backup and delete JSON files
    echo.
) else (
    echo.
    echo ========================================
    echo MIGRATION FAILED!
    echo ========================================
    echo Please check the error messages above.
    echo.
)

pause
