#!/bin/bash

echo "🚀 Starting local deployment..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip and install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check if .env file exists, create if not
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file..."
    echo "GEMINI_API_KEY=your_api_key_here" > .env
    echo "⚠️ Please update the GEMINI_API_KEY in .env file"
fi

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | xargs)
fi

echo "✅ Setup complete!"
echo "🏃 Starting application..."
python app.py