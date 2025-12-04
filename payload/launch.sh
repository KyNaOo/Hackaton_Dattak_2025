#!/bin/bash

# Launch script for Flask server with ngrok tunnel

echo "=========================================="
echo "Flask Server with ngrok Launcher"
echo "=========================================="
echo ""

# Check if Flask is installed
if ! python -c "import flask" 2>/dev/null; then
    echo "Error: Flask is not installed."
    echo "Please install it with: pip install flask"
    exit 1
fi

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "Error: ngrok is not installed."
    echo "Please install it following the instructions in README.md"
    exit 1
fi

# Check if ngrok is authenticated
if ! ngrok config check &> /dev/null; then
    echo "Warning: ngrok might not be authenticated."
    echo "If you get an authentication error, please run:"
    echo "  ngrok config add-authtoken YOUR_TOKEN_HERE"
    echo ""
fi

# Create necessary directories
mkdir -p log
mkdir -p images

# Check if image exists
if [ ! -f "images/rickroll.jpg" ]; then
    echo "Warning: images/rickroll.jpg not found."
    echo "The server will return 404 for image requests."
    echo ""
fi

# Start Flask server in background
echo "Starting Flask server on port 5000..."
python src/server.py > log/flask.log 2>&1 &
FLASK_PID=$!
echo "Flask server started (PID: $FLASK_PID)"

# Wait for Flask to start
sleep 3

# Check if Flask is running
if ! ps -p $FLASK_PID > /dev/null; then
    echo "Error: Flask server failed to start. Check log/flask.log for details."
    exit 1
fi

# Start ngrok tunnel
echo "Starting ngrok tunnel..."
ngrok http 5000 > log/ngrok.log 2>&1 &
NGROK_PID=$!
echo "ngrok started (PID: $NGROK_PID)"

# Wait for ngrok to establish tunnel
sleep 3

# Check if ngrok is running
if ! ps -p $NGROK_PID > /dev/null; then
    echo "Error: ngrok failed to start. Check log/ngrok.log for details."
    kill $FLASK_PID 2>/dev/null
    exit 1
fi

# Get the public URL
echo ""
echo "Fetching public URL..."
sleep 1

PUBLIC_URL=$(curl -s http://localhost:4040/api/tunnels | python -c "import sys, json; print(json.load(sys.stdin)['tunnels'][0]['public_url'])" 2>/dev/null)

if [ -n "$PUBLIC_URL" ]; then
    echo ""
    echo "=========================================="
    echo "✓ Server is running!"
    echo "=========================================="
    echo "Public URL: $PUBLIC_URL"
    echo "Monitoring URL:  http://localhost:5000/logs"
    echo ""
    echo "Logs:"
    echo "  - Client access: log/client_access.log"
    echo "  - Flask output:  log/flask.log"
    echo "  - ngrok output:  log/ngrok.log"
    echo ""
    echo "Process IDs:"
    echo "  - Flask: $FLASK_PID"
    echo "  - ngrok: $NGROK_PID"
    echo ""
    echo "To stop all services, run:"
    echo "  ./stop.sh"
    echo "  or manually: kill $FLASK_PID $NGROK_PID"
    echo "=========================================="

    # Save PIDs for stop script
    echo "$FLASK_PID" > log/flask.pid
    echo "$NGROK_PID" > log/ngrok.pid

else
    echo "Warning: Could not retrieve public URL."
    echo "Check ngrok dashboard at: http://localhost:4040"
    echo ""
    echo "Processes are running:"
    echo "  - Flask PID: $FLASK_PID"
    echo "  - ngrok PID: $NGROK_PID"
fi

echo ""
echo "Press Ctrl+C or run ./stop.sh to stop the services."
