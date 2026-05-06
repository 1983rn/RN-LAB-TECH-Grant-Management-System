@echo off
TITLE Sync Changes to GitHub
echo ========================================
echo PREPARING TO PUSH CHANGES TO GITHUB
echo ========================================
echo.

echo 1. Checking git status...
git status
echo.

echo 2. Adding changes...
git add .
echo.

echo 3. Committing changes...
git commit -m "Refactor authentication, optimize loader visuals, and fix budget persistence"
echo.

echo 4. Pushing to GitHub (main branch)...
git push origin main
echo.

echo ========================================
echo SYNC COMPLETE
echo ========================================
echo.
pause
