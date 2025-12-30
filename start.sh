#!/bin/bash

# Alter Lab Startup Script

echo "🔮 Starting Alter Lab..."
echo ""

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "⚠️  Ollama not running. Starting Ollama..."
    brew services start ollama
    sleep 3
fi

# Check Ollama status
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama is running"
else
    echo "❌ Ollama failed to start. Please run: brew services start ollama"
    exit 1
fi

# Start the FastAPI server
echo ""
echo "Starting Alter Lab server on http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""

cd "$(dirname "$0")"
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
