@echo off
REM Script to push myfinlab to GitHub
REM Make sure you've created the repository at: https://github.com/new

echo ========================================
echo Pushing MyFinLab to GitHub
echo ========================================
echo.

cd /d "%~dp0"

echo Step 1: Verifying git remote...
git remote -v
echo.

echo Step 2: Pushing to GitHub...
echo.
git push -u myfinlab master

echo.
echo ========================================
echo Done! Your repository is at:
echo https://github.com/Jn316Alpha/myfinlab
echo ========================================
echo.
echo To install from GitHub, run:
echo pip install git+https://github.com/Jn316Alpha/myfinlab.git
echo.

pause
