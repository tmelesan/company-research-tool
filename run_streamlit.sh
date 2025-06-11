#!/bin/bash

# Company Research Tool - Streamlit Web App Launcher
echo "🚀 Starting Company Research Tool Web Interface..."
echo ""

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment is active: $VIRTUAL_ENV"
else
    echo "⚠️  Virtual environment not detected. Activating..."
    if [[ -f "venv/bin/activate" ]]; then
        source venv/bin/activate
        echo "✅ Virtual environment activated"
    else
        echo "❌ Virtual environment not found. Please run:"
        echo "   python -m venv venv"
        echo "   source venv/bin/activate"
        echo "   pip install -r requirements.txt"
        exit 1
    fi
fi

# Check if Streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit not found. Installing dependencies..."
    pip install -r requirements.txt
fi

# Check for API key
if [[ -z "$GEMINI_API_KEY" ]]; then
    echo ""
    echo "🔑 No GEMINI_API_KEY environment variable found."
    echo "You can either:"
    echo "1. Set it now: export GEMINI_API_KEY='your-api-key'"
    echo "2. Enter it in the web interface when prompted"
    echo ""
    read -p "Press Enter to continue or Ctrl+C to exit and set the API key..."
fi

echo ""
echo "🌐 Starting Streamlit web interface..."
echo "📱 The app will open in your default web browser"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Start Streamlit app
streamlit run streamlit_app.py --server.port 8501 --server.address localhost

echo ""
echo "👋 Thanks for using the Company Research Tool!"
