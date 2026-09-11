@echo off
setlocal enabledelayedexpansion

title Building Jankalyan Blood Bank Standalone Executable

echo =====================================================================
echo   Jankalyan Blood Bank Digital System (QF/JKRP/18)
echo   PyInstaller Automated Windows Build Script
echo =====================================================================
echo.

:: 1. Detect Python executable (check virtual environment first, then system python)
set "PYTHON_EXE="

if exist "%~dp0myvenv\Scripts\python.exe" (
    set "PYTHON_EXE=%~dp0myvenv\Scripts\python.exe"
    echo [*] Using virtual environment Python: !PYTHON_EXE!
) else if exist "%~dp0venv\Scripts\python.exe" (
    set "PYTHON_EXE=%~dp0venv\Scripts\python.exe"
    echo [*] Using virtual environment Python: !PYTHON_EXE!
) else (
    where python >nul 2>nul
    if %errorlevel% equ 0 (
        set "PYTHON_EXE=python"
        echo [*] Using System Python
    ) else (
        echo [ERROR] Python was not found in PATH or local virtualenv!
        echo Please ensure Python 3.10+ is installed and added to PATH.
        echo.
        pause
        exit /b 1
    )
)

echo.
:: 2. Install / Verify Dependencies
echo [*] Checking and installing required dependencies...
"%PYTHON_EXE%" -m pip install -r "%~dp0requirements.txt"
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install requirements. Please check your internet connection or python environment.
    echo.
    pause
    exit /b %errorlevel%
)

echo.
:: 3. Clean previous build artifacts
echo [*] Cleaning old build directories...
if exist "%~dp0build" rd /s /q "%~dp0build"
if exist "%~dp0dist\JankalyanBloodBank" rd /s /q "%~dp0dist\JankalyanBloodBank"

echo.
:: 4. Run PyInstaller Build
echo [*] Running PyInstaller with bloodbank.spec...
"%PYTHON_EXE%" -m PyInstaller --noconfirm "%~dp0bloodbank.spec"

if %errorlevel% equ 0 (
    echo.
    echo =====================================================================
    echo   BUILD SUCCESSFUL!
    echo =====================================================================
    echo [OK] Application Directory : %~dp0dist\JankalyanBloodBank\
    echo [OK] Executable Binary     : %~dp0dist\JankalyanBloodBank\JankalyanBloodBank.exe
    echo.
    echo Next Steps:
    echo 1. Test the application by running:
    echo    "%~dp0dist\JankalyanBloodBank\JankalyanBloodBank.exe"
    echo.
    echo 2. To compile the Windows Setup Installer (.exe):
    echo    Open inno_setup.iss in Inno Setup Compiler and press Ctrl+F9
    echo =====================================================================
) else (
    echo.
    echo =====================================================================
    echo   [ERROR] Build failed! Please review the error messages above.
    echo =====================================================================
)

echo.
pause
