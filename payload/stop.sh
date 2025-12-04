#!/bin/bash

# Stop script for Flask server and ngrok

echo "=========================================="
echo "Stopping Flask Server and ngrok"
echo "=========================================="
echo ""

STOPPED=0

# Stop using saved PIDs
if [ -f "log/flask.pid" ]; then
    FLASK_PID=$(cat log/flask.pid)
    if ps -p $FLASK_PID > /dev/null 2>&1; then
        echo "Stopping Flask server (PID: $FLASK_PID)..."
        kill $FLASK_PID
        STOPPED=1
    fi
    rm log/flask.pid
fi

if [ -f "log/ngrok.pid" ]; then
    NGROK_PID=$(cat log/ngrok.pid)
    if ps -p $NGROK_PID > /dev/null 2>&1; then
        echo "Stopping ngrok (PID: $NGROK_PID)..."
        kill $NGROK_PID
        STOPPED=1
    fi
    rm log/ngrok.pid
fi

# Fallback: kill by process name
if [ $STOPPED -eq 0 ]; then
    echo "No PID files found. Searching for processes..."

    # Find and kill Flask server
    FLASK_PIDS=$(pgrep -f "python.*src/server.py")
    if [ -n "$FLASK_PIDS" ]; then
        echo "Stopping Flask server processes: $FLASK_PIDS"
        kill $FLASK_PIDS 2>/dev/null
        STOPPED=1
    fi

    # Find and kill ngrok
    NGROK_PIDS=$(pgrep ngrok)
    if [ -n "$NGROK_PIDS" ]; then
        echo "Stopping ngrok processes: $NGROK_PIDS"
        kill $NGROK_PIDS 2>/dev/null
        STOPPED=1
    fi
fi

if [ $STOPPED -eq 1 ]; then
    echo ""
    echo "✓ Services stopped successfully."
else
    echo "No running services found."
fi

echo "=========================================="
