@echo off
REM Script to upload myfinlab to PyPI
REM
REM Before running:
REM 1. Create PyPI account at https://pypi.org/account/register/
REM 2. Create API token at https://pypi.org/manage/account/token/
REM 3. Copy your token and paste it when prompted

echo ========================================
echo Upload MyFinLab to PyPI
echo ========================================
echo.
echo You will need your PyPI API token.
echo Get it from: https://pypi.org/manage/account/token/
echo.
echo Username: __token__
echo Password: (paste your token starting with pypi-...)
echo.

cd /d "%~dp0"

echo Uploading to PyPI...
echo.

twine upload dist/*

echo.
echo ========================================
echo If successful, your package is at:
echo https://pypi.org/project/myfinlab/
echo ========================================
echo.
echo Install with: pip install myfinlab
echo.

pause
