REM ========================================
REM run.bat - Windows Run Script
REM ========================================
@echo off
echo.
echo ================================================
echo   Starting Cyber Threat Detector...
echo ================================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [ERROR] Virtual environment not found!
    echo.
    echo Please run setup first:
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

REM Create logs directory
if not exist "logs\" mkdir logs

REM Check if app.py exists
if not exist "app.py" (
    echo [ERROR] app.py not found!
    echo Make sure you're in the correct directory.
    pause
    exit /b 1
)

REM Start the application
echo [*] Starting application...
echo.
echo ================================================
echo    Dashboard: http://localhost:5000
echo ================================================
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause

REM ========================================
REM test.bat - Windows Test Script
REM ========================================
@echo off
echo.
echo ================================================
echo   Cyber Threat Detector - Test Suite
echo ================================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [ERROR] Virtual environment not found!
    echo Please run: run.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if test file exists
if not exist "test_detector.py" (
    echo [ERROR] test_detector.py not found!
    pause
    exit /b 1
)

REM Check if server is running
echo [*] Checking if server is running...
curl -s http://localhost:5000/api/stats >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Server is not running!
    echo.
    echo Please start the server first:
    echo   run.bat
    echo.
    echo Or in a separate terminal:
    echo   venv\Scripts\activate
    echo   python app.py
    echo.
    pause
    exit /b 1
)

echo [*] Server is running!
echo.

REM Run the test script with all arguments
python test_detector.py %*

pause