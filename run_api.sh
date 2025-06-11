#!/bin/bash

# Company Research Tool - FastAPI Server Launcher
# This script starts the FastAPI REST API server

echo "🚀 Starting Company Research Tool FastAPI Server..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check for API key
if [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠️  Warning: GEMINI_API_KEY environment variable not set"
    echo "   Please set it before making API calls:"
    echo "   export GEMINI_API_KEY='your-api-key-here'"
    echo ""
fi

# Start the FastAPI server
echo "🌐 Starting FastAPI server on http://localhost:8000"
echo "📚 API Documentation available at http://localhost:8000/docs"
echo "📖 Alternative docs at http://localhost:8000/redoc"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the server with uvicorn
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
