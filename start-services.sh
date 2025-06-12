#!/bin/bash
set -e

echo "🚀 Starting Company Research Tool Services..."

# Start FastAPI server in background
echo "📡 Starting API Server on port 8000..."
uvicorn api:app --host 0.0.0.0 --port 8000 &
API_PID=$!

# Start Streamlit web server in background
echo "🌐 Starting Web Server on port 8501..."
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0 &
WEB_PID=$!

# Function to handle shutdown
shutdown() {
    echo "🛑 Shutting down services..."
    kill $API_PID $WEB_PID 2>/dev/null || true
    wait $API_PID $WEB_PID 2>/dev/null || true
    echo "✅ Services stopped"
    exit 0
}

# Set up signal handlers
trap shutdown SIGTERM SIGINT

echo "✅ Both services started successfully!"
echo "📡 API Server: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "🌐 Web Interface: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for background processes
wait $API_PID $WEB_PID
