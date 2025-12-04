# Flask Image Server with Client Logging

A simple Flask server that serves an image and logs detailed client information for every request.

## Features

- Serves a webpage with an embedded image
- Logs all client information including:
  - IP address
  - User agent (browser/device info)
  - Referer
  - Request headers
  - Timestamp
- Saves logs in both human-readable and JSON formats
- Can be exposed to the internet using ngrok

## Prerequisites

- Python 3.x
- Flask
- ngrok (for internet exposure)

## Installation

1. Install Flask:
```bash
pip install flask
```

2. Install ngrok:
```bash
# For Ubuntu/Debian
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update
sudo apt install ngrok
```

3. Set up ngrok authentication:
   - Sign up at https://dashboard.ngrok.com/signup
   - Get your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken
   - Configure ngrok:
   ```bash
   ngrok config add-authtoken YOUR_TOKEN_HERE
   ```

## Quick Start

### Easy Launch (Recommended)

The easiest way to start everything:

```bash
./launch.sh
```

This will:
- Start the Flask server on port 5000
- Create an ngrok tunnel to expose it to the internet
- Display the public URL
- Save all logs to the `log/` directory

To stop all services:

```bash
./stop.sh
```

### Manual Usage

#### Running Locally

1. Make sure you have an image at `images/rickroll.jpg` (or update the path in `src/server.py`)

2. Start the Flask server:
```bash
python src/server.py
```

3. Access locally at:
   - http://localhost:5000

#### Exposing to the Internet

1. Start the Flask server (if not already running):
```bash
python src/server.py
```

2. In a new terminal, start ngrok:
```bash
ngrok http 5000
```

3. ngrok will display a public URL like:
   ```
   Forwarding: https://xxxx-xxxx-xxxx.ngrok-free.app -> http://localhost:5000
   ```

4. Share this public URL with anyone on the internet!

## Viewing Logs

Client access information is logged to the `log/` directory:

- **log/client_access.log** - Human-readable text format
  ```bash
  cat log/client_access.log
  # or watch in real-time
  tail -f log/client_access.log
  ```

- **log/client_access.json** - JSON format (one entry per line)
  ```bash
  cat log/client_access.json
  # or pretty print with jq
  cat log/client_access.json | jq .
  ```

## Endpoints

- **/** - Main page displaying the image
- **/image** - Direct image endpoint

## Log Format

Each client access logs:
- Timestamp
- IP Address
- User Agent
- Referer
- HTTP Method
- Full Request Path
- All HTTP Headers

## Running in Background

To keep both services running:

```bash
# Start Flask server in background
python src/server.py &

# Start ngrok in background
ngrok http 5000 &
```

To stop:
```bash
# Find process IDs
ps aux | grep "python src/server.py"
ps aux | grep ngrok

# Kill processes
kill <PID>
```

## Security Notes

- This is a development server, not suitable for production
- All client information is logged, including sensitive headers
- The ngrok free tier URL is temporary and changes on restart
- Be cautious about what information you collect and how you store it

## File Structure

```
.
├── src/
│   └── server.py          # Main Flask application
├── launch.sh              # Script to start Flask + ngrok
├── stop.sh                # Script to stop all services
├── images/
│   └── rickroll.jpg       # Image to serve
├── log/
│   ├── client_access.log  # Human-readable client logs
│   ├── client_access.json # JSON format client logs
│   ├── flask.log          # Flask server output
│   ├── ngrok.log          # ngrok output
│   ├── flask.pid          # Flask process ID
│   └── ngrok.pid          # ngrok process ID
└── README.md              # This file
```

---

**Original Project Note:**
Creation d'une idée de solution cyber utile pour les assurés Dattak, avec une présentation et un POC.
