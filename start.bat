@echo off
echo Setting up AI Meal Plan Assistant...
echo.

REM Check if GEMINI_API_KEY is set
if "%GEMINI_API_KEY%"=="" (
    echo ERROR: GEMINI_API_KEY environment variable is not set.
    echo.
    echo Please set your Google GenAI API key:
    echo set GEMINI_API_KEY=your_api_key_here
    echo.
    echo Get your API key from: https://makersuite.google.com/app/apikey
    echo.
    pause
    exit /b 1
)

echo ✓ GEMINI_API_KEY is set
echo.

REM Test dependencies
echo Testing dependencies...
python test_setup.py
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Dependency test failed
    pause
    exit /b 1
)

echo.
echo Starting the AI Meal Plan Assistant...
echo Open your browser to: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py
