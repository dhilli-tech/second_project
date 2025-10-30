@echo off
echo 🚀 Starting local deployment...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is required but not installed.
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip and install dependencies
echo 📥 Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

REM Check if .env file exists, create if not
if not exist ".env" (
    echo ⚙️ Creating .env file...
    echo GEMINI_API_KEY=your_api_key_here > .env
    echo ⚠️ Please update the GEMINI_API_KEY in .env file
)

echo ✅ Setup complete!
echo 🏃 Starting application...
python app.py

pause